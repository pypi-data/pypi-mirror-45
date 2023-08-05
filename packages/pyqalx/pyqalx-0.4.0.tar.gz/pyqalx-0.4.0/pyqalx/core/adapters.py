"""
.. autoclass:: QalxSession
    :members:

.. autoclass:: QalxAdapter
    :members:
"""
import copy
import json
import logging
import platform
import time
from logging import getLogger
from types import MethodType

from pyqalx.config import UserConfig, BotConfig
from pyqalx.core import QalxNoGUIDError
from pyqalx.core.entities import Bot, QalxListEntity, Set, Item, Group, Queue
from pyqalx.core.entities.worker import Worker
from pyqalx.core.errors import QalxError, QalxAPIResponseError, \
    QalxMultipleEntityReturned, QalxInvalidSession, \
    QalxEntityNotFound, QalxConfigError, QalxEntityTypeNotFound, QalxFileError
from pyqalx.core.log import configure_logging
from pyqalx.core.signals import QalxSignal, QalxWorkerSignal, QalxBotSignal
from pyqalx.transport import PyQalxAPI

logger = logging.getLogger(__name__)


class QalxAdapter(object):
    """
    The base class for a QalxAdapter. An adapter is the interface for the
    entity to the rest api.  This allows us to have a consistent interface
    across all entity types.
    Can be instatiated in two ways:

    QalxAdapter(entity_type='item') -> Returns a QalxItem() instance
    QalxItem() -> Retuns a QalxItem() instance
    """

    def __init__(self, session, *args, **kwargs):
        # We don't need the entity_type after instantiation - it's used in
        # __new__ to determine what subclass of QalxAdapter to use
        kwargs.pop('entity_type', None)

        if not isinstance(session, QalxSession):
            raise QalxInvalidSession(f'`qalx_session` should be an instance of'
                                     f' `{QalxSession}`.  '
                                     f'Got `{type(session)}`')
        self.session = session

        super(QalxAdapter, self).__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        """
        Overriding the __new__ method allows a user to call
        QalxAdapter(entity_type='item') and for them to get the correct
        subclass of `QalxAdapter` back.  This makes it much easier to just use
        `QalxAdapter` on (for example) a Bot and just instantiate it with the
        `entity_type` string that is in the body of messages.
        If a user wants to instantiate a specific subclass they can do so
        by not specifying the entity_type
        """
        instantiate_as_class = cls

        if 'entity_type' in kwargs.keys():
            entity_type = kwargs['entity_type'].lower()

            def _get_all_subclasses(_cls):
                # Recursively gets all the subclasses of QalxAdapter
                all_subclasses = []

                for subclass in _cls.__subclasses__():
                    all_subclasses.append(subclass)
                    all_subclasses.extend(_get_all_subclasses(subclass))

                return set(all_subclasses)

            entity_classes = list(filter(lambda x: hasattr(x, 'entity_class')
                                         and x.entity_class.entity_type == entity_type,
                                         _get_all_subclasses(QalxAdapter)))
            if len(entity_classes) == 0:
                raise QalxEntityTypeNotFound(entity_type + " not found.")
            elif len(entity_classes) >= 2:
                raise QalxMultipleEntityReturned(entity_type +
                                                 " matches more than 1 class.")
            else:
                instantiate_as_class = entity_classes[0]
        return super(QalxAdapter, cls).__new__(instantiate_as_class)

    def __getattribute__(self, item):
        """
        Certain methods can only be calld by sessions with a UserConfig or a
        BotConfig.  The API will return a 403 Permission Denied
        but this method handles showing the user a more useful error message
        """
        attr = super(QalxAdapter, self).__getattribute__(item)
        if callable(attr) and isinstance(attr, MethodType):
            # This is a method on `QalxBot`.  Check the config
            # is correct for the method we are calling
            def _msg(expected_class, actual_class):
                return f"Method `{item}` on `{self.__class__}` " \
                    f"must be called via a session with a `{expected_class}`" \
                    f"instance.  Got `{actual_class}`"
            is_user_config = isinstance(self.session.config, UserConfig)
            is_bot_config = isinstance(self.session.config, BotConfig)

            if item in getattr(self, '_user_only_methods', []) and not is_user_config:
                raise QalxConfigError(_msg(UserConfig, BotConfig))
            if item in getattr(self, '_bot_only_methods', []) and not is_bot_config:
                raise QalxConfigError(_msg(BotConfig, UserConfig))
        return attr

    def _process_api_request(self, method, *args, **kwargs):
        """calls to pyqalxapi

        :param method: http method required
        :param args: args to be passed to endpoint method
        :param kwargs: kwargs to be passed to endpoint method
        :returns: `dict` containing API resource data
        """
        
        if kwargs.get('meta', None) is None:
            # meta is optional but must always be sent through as a dict
            kwargs['meta'] = {}

        input_file = kwargs.pop('input_file', None)

        try:
            json.dumps(kwargs)
        except (TypeError, OverflowError):
            raise QalxError("One of the keyword arguments is "
                            "not JSON serializable")

        try:
            endpoint = getattr(self.session.rest_api, method.lower())
            logger.debug(str(endpoint))
        except AttributeError:
            raise QalxError(f"{method} not recognised.")

        if input_file is not None:
            file_name = kwargs.pop("file_name", None)
            success, data = endpoint(*args,
                                     input_file=input_file,
                                     file_name=file_name,
                                     json=kwargs)
        else:
            success, data = endpoint(*args, json=kwargs)

        if success:
            return data
        m = "API request error, message:\n\n-vvv-\n\n"
        m += "\n".join([f"{k}: {v}" for k, v in data.items()])
        m += "\n\n-^^^-"
        raise QalxAPIResponseError(m)

    @classmethod
    def detail_endpoint(cls, guid, *args, **kwargs):
        """
        The endpoint for interfacing with a single
        instance of `self.entity_class`
        """
        return f"{cls.entity_class.entity_type}/{guid}"

    @classmethod
    def list_endpoint(cls, *args, **kwargs):
        """
        The endpoint for interfacing with multiple instances of
        `self.entity_class`
        """
        return cls.entity_class.entity_type

    def get_keys_to_save(self, entity):
        """
        When saving an entity we don't want to save every key
        """
        # info & guid are both read only
        # status should only be saved via `update_status` (if available)
        return {k: entity[k] for k in entity
                if k not in ('info', 'guid', 'status')}

    def add(self, **kwargs):
        """
        Adds a new instance of `self.entity_class`.  Provide valid `kwargs`
        for the object you are trying to create

        :return: An instance of `self.entity_class`
        """
        response = self._process_api_request('post',
                                             self.list_endpoint(**kwargs),
                                             **kwargs)
        # TODO: Should we return packable entiies in an unpacked state?
        return self.entity_class(response)

    def get(self, guid, *args, **kwargs):
        """
        Gets an instance of `self.entity_class` by the given guid.

        :param guid: The guid of the entity you want to get
        :return: An instance of `self.entity_class`
        """
        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        resp = self._process_api_request('get', endpoint, *args, **kwargs)
        logger.debug(f"get {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        return self.entity_class(resp)

    def list(self, sort=None, skip=0, limit=25, many=True, **kwargs):
        """
        Method for listing entities. If `many=False` will attempt to return
        a single entity and will error if any more/less than 1 is found

        :param sort: The keys we should sort by
        :param skip: The number of results we should skip (offset) by
        :param limit: How many results we should limit the response to
        :param many: Should many entities be returned or just a single one
        :param kwargs: kwargs to query by
        :return:
        """
        # The list endpoint might need specific kwargs but we don't want
        # to use those kwargs when querying the endpoint
        list_endpoint_kwargs = kwargs.pop('list_endpoint_kwargs', {})
        list_endpoint = self.list_endpoint(**list_endpoint_kwargs)
        logger.debug(f"list {self.entity_class.entity_type} with {list_endpoint}")
        resp = self._process_api_request('get',
                                         list_endpoint,
                                         sort=sort,
                                         skip=skip,
                                         limit=limit,
                                         **kwargs)
        entities = QalxListEntity(self.entity_class, resp)

        if many is False:

            # We are expecting only a single entity.
            entities = entities['data']
            if len(entities) > 1:
                entities_str = "\n".join([str(q) for q in entities])
                raise QalxMultipleEntityReturned("Expected one but got "
                                                 "{}:\n{}".format(len(entities),
                                                                  entities_str))
            elif entities:
                return entities[0]
            else:
                raise QalxEntityNotFound(self.entity_class.entity_type +
                                         " not found.")
        return entities

    def reload(self, entity):
        """
        Reloads the current entity from the API

        :return: A refreshed instance of `self.entity`
        """
        return self.get(entity['guid'])

    def save(self, entity, *args, **kwargs):
        """
        Saves `self.entity` to the database.

        :return: The updated instance of `self.entity`
        """
        if not entity.get("guid"):
            raise QalxNoGUIDError("No guid.")
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        keys_to_save = self.get_keys_to_save(entity=entity)
        logger.debug(f"save {self.entity_class.entity_type} with guid {guid} with {endpoint}")

        resp = self._process_api_request('patch', endpoint, **keys_to_save)
        return self.entity_class(resp)

    def archive(self, entity, *args, **kwargs):
        """
        Archives `self.entity`

        :return: The archived instance of `self.entity`
        """
        guid = entity['guid']
        detail_endpoint = self.detail_endpoint(guid=guid,
                                               *args, **kwargs)
        endpoint = f"{detail_endpoint}/archive"
        logger.debug(f"archive {self.entity_class.entity_type} with guid {guid} with {endpoint}")

        resp = self._process_api_request('patch', endpoint)
        return self.entity_class(resp)


class QalxUnpackableAdapter(QalxAdapter):
    """
    A qalx adapter for unpackable entities (Set, Group)
    """

    @property
    def kids(self):
        """
        The key that the child entities live in
        """
        return self.child_entity_class.entity_type + 's'

    def _child_list_response(self, child_adapter, guid_query, entity):
        return child_adapter.list(guid=guid_query)

    def _get_child_entities(self, entity):
        """
        Gets all the child entities for the given entity.  Handles chunking
        the children up into blocks to guard against sending a request that is
        too large.  Also handles the paginated result coming back from the
        `list` endpoint.  Does a `list` lookup for self.child_entity_class
        filtering on `guid` of the children to reduce the amount of queries

        :param entity: The entity we want to unpack
        :return: The child entities as a list
        """
        kids = entity[self.kids]
        if isinstance(kids, dict):
            # Handles Sets, Groups
            kids_guids = list(kids.values())
        elif isinstance(kids, list):
            # Handles Bot
            kids_guids = kids
        else:
            # This won't happen unless someone overrides this method or
            # has `self.kids` in an unhandled format
            raise QalxError(f'`self.kids` key on `entity` must be dict or '
                            f'list. Got `{type(kids)}`')

        unpacked_entities = []
        child_adapter = QalxAdapter(session=self.session,
                                    entity_type=self.child_entity_class.entity_type)

        for _page in entity._chunks(kids_guids, chunk_size=100):
            # Chunk to avoid hitting maximum request size
            guid_values = ','.join(filter(None, _page))
            guid_query = f'in=({guid_values})'
            _resp = self._child_list_response(child_adapter=child_adapter,
                                              guid_query=guid_query,
                                              entity=entity)
            unpacked_entities += _resp['data']
            while _resp['query']['next'] is not None:
                # We got a paginated response so keep going through the pages
                # until we exhaust this chunk of data
                logger.debug(f"get {self.entity_class.entity_type} with {_resp['query']['next']}")
                _resp = self._process_api_request('get',
                                                  _resp['query']['next'])
                unpacked_entities += QalxListEntity(self.child_entity_class, _resp)['data']
        return unpacked_entities

    def _unpacked_entities_to_valid_children(self, entity, unpacked_entities):
        """
        Converts a list of `unpacked_entities` into valid child entities
        for the given entity.

        :param entity: The entity that has kids we want to unpack
        :param unpacked_entities: The unpacked child entities that need to be
                                  stitched into the entity
        :return: The unpacked entities in the correct format to be assigne to
                 `entity[self.kids]`
        """
        to_return = {}
        for key, item_guid in entity[self.kids].items():
            for child_entity in unpacked_entities:
                if item_guid == child_entity['guid']:
                    child_entity_adapter = QalxAdapter(session=self.session,
                                                       entity_type=child_entity.entity_type)
                    if hasattr(child_entity_adapter, 'child_entity_class'):
                        # The child entity has a child adapter of it's own.
                        # Attempt unpack. This can occur if we are unpacking
                        # a Group as we may need to unpack the Sets on the
                        # Group
                        to_return[key] = child_entity_adapter._attempt_unpack(child_entity)
                    else:
                        to_return[key] = child_entity
        return to_return

    def _attempt_unpack(self, entity):
        """
        For the given entity will attempt
        to unpack the child_entity data that it contains

        :entity: The entity we want to unpack
        :return: The entity instance with the child_entity objects unpacked
        """

        should_unpack = self.session.config.getboolean(
            "UNPACK_" + self.entity_class.entity_type.upper())

        if should_unpack and self.kids in entity:
            # `self.kid` might not be there if we have specified a subset
            # of fields
            unpacked_entities = self._get_child_entities(entity)
            entity[self.kids] = self._unpacked_entities_to_valid_children(
                entity=entity,
                unpacked_entities=unpacked_entities)
        return entity

    def get_keys_to_save(self, entity):
        """
        Unpackable entities will have unpacked data stored on them that we have
        to submit as packed data
        """
        keys_to_save = super(QalxUnpackableAdapter,
                             self).get_keys_to_save(entity=entity)
        keys_to_save[self.kids] = {k: str(i['guid']) for k, i in
                                   keys_to_save[self.kids].items()}
        return keys_to_save

    def get(self, guid, *args, **kwargs):
        """
        Unpackable entities need to be unpacked after we `get` them

        :param guid: The `guid` of the entity we are getting
        :return: An unpacked entity
        """
        entity = super(QalxUnpackableAdapter, self).get(guid=guid,
                                                        *args, **kwargs)
        entity = self._attempt_unpack(entity)
        return entity

    def list(self, many=True, *args, **kwargs):
        entities = super(QalxUnpackableAdapter, self).list(many=many,
                                                           *args,
                                                           **kwargs)
        if many is False:
            # Only unpack a list view if we have a single entity
            entities = self._attempt_unpack(entities)
        return entities

    def save(self, entity, *args, **kwargs):
        """
        When saving an unpacked entity we need to pack the kids.  To save
        having to unpack them again we just save the original kids and replace
        them with the packed values after saving
        """
        original_kids = copy.deepcopy(entity[self.kids])
        entity = super(QalxUnpackableAdapter, self).save(entity=entity)
        entity[self.kids] = original_kids
        return entity


class QalxSignalAdapter(QalxAdapter):
    """
    Bots and Workers have signals that are used to determine when to stop
    processing data.  This class provides that shared functionality
    """
    def get_signal(self, entity, *args, **kwargs):
        """
        Gets just the `signal` field from the entity and then parses that
        into the `signal_class`
        """
        entity = self.get(guid=entity['guid'], fields='signal', *args,
                          **kwargs)
        signal = self.signal_class(entity)
        return signal

    def terminate(self, entity, *args, **kwargs):
        """
        Updates the entity with a terminate signal
        """
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        logger.debug(f"terminate {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        signal = self.signal_class._terminate_signal(*args, **kwargs)

        self._process_api_request('patch', endpoint, signal=signal)

    def _stop_or_resume(self, entity, stop, **kwargs):
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        signal = self.signal_class._stop_signal(stop)
        logger.debug(f"signal {signal} {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        self._process_api_request('patch', endpoint, signal=signal)

    def stop(self, entity, **kwargs):
        """
        Updates the entity with a stop signal
        """
        self._stop_or_resume(entity, stop=True, **kwargs)

    def resume(self, entity, **kwargs):
        """
        Updates the entity with a resume signal
        """
        self._stop_or_resume(entity, stop=False, **kwargs)


class QalxItem(QalxAdapter):
    entity_class = Item

    def add(self, **kwargs):
        """
        Adds an `Item` instance.  Ensures that `data` is present and is a dict

        :param kwargs: The kwargs that we are adding to the `Item`
        :return: A newly created `Item` instance
        """
        if isinstance(kwargs.get('data'), dict):
            return super(QalxItem, self).add(**kwargs)
        else:
            raise QalxError(
                "Only item data in dict format can be added with this "
                "function. To add a file try add_file ")

    def add_file(self, input_file, file_name="", **kwargs):
        """adds a file to qalx with optional data and metadata

        :param input_file: input file path or stream
        :param file_name: input file name
        :param data: (optional) data associated with the file
        :param meta: (optional) additional data about the item
        :return: pyqalx.core.Item
        """
        if 'data' not in kwargs.keys():
            kwargs['data'] = {}

        if self.session.rest_api.is_filestream(input_file) and not file_name:
            raise QalxFileError('You must supply a file name when supplying'
                                ' a file stream')
        return self.add(input_file=input_file, file_name=file_name, **kwargs)


class QalxSet(QalxUnpackableAdapter):
    entity_class = Set
    child_entity_class = Item

    def add(self, items, **kwargs):
        """
        When adding a `Set` ensure that the items we post to the api are in the
        format {<key>: <guid>}

        :param items: A dictionary of Items to create on the set
        :return: A newly created `Set` instance
        """
        items = {key: str(item['guid']) for key, item in items.items()}
        return super(QalxSet, self).add(items=items, **kwargs)


class QalxGroup(QalxUnpackableAdapter):
    entity_class = Group
    child_entity_class = Set

    def add(self, sets, **kwargs):
        """
        When adding a `Group` ensure that the sets we post to the api are in
        the format {<key>: <guid>}

        :param sets: A dictionary of Sets to create on the group
        :return: A newly created `Group` instance
        """
        sets = {key: dataset['guid'] for key, dataset in sets.items()}
        return super(QalxGroup, self).add(sets=sets, **kwargs)


class QalxQueue(QalxAdapter):
    entity_class = Queue
    _bot_only_methods = ['get_messages']

    @property
    def _queue_params(self):
        """
        The configurable parameters for a `Queue`
        :return:
        """
        return {
            'VisibilityTimeout': int(self.session.config['MSG_BLACKOUTSECONDS'])
        }

    def add(self, name, **kwargs):
        """
        Queues are created with a name.  This name is stored in the metadata
        of the `Queue` instance

        :param name: The name we want to assign the Queue
        :type name: str
        :param kwargs: Any other kwargs we are setting on the Queue
        :return: A newly created `Queue` instance
        """
        return super(QalxQueue, self).add(parameters=self._queue_params,
                                          name=name,
                                          **kwargs)

    def get_messages(self, queue):
        """
        Gets the messages on the `Queue` instance

        :return: A list of `QueueMessage` instances
        """
        config = self.session.config
        max_msgs = int(config["Q_MSGBATCHSIZE"])
        visibility = int(config["MSG_BLACKOUTSECONDS"])
        waittime = int(config["MSG_WAITTIMESECONDS"])

        message = queue.get_messages(max_msgs, visibility, waittime)
        return message

    def get_by_name(self, name):
        """a single queue by name

        :param name: name of queue
        :type name: str
        :return: pyqalx.core.entities.Queue
        :raises: pyqalx.errors.QalxReturnedMultipleError,
                 pyqalx.errors.QalxEntityNotFound
        """
        return self.list(many=False, name=name)

    def get_or_create(self, name, meta=None):
        """
        Gets a Queue by the given name or creates it if it doesn't exist

        :param name:
        :type name: str
        :param meta: metadata about the queue
        :return: pyqalx.core.entities.Queue
        """
        try:
            return self.get_by_name(name=name)
        except QalxEntityNotFound:
            return self.add(name, meta=meta)


class QalxBot(QalxUnpackableAdapter,
              QalxSignalAdapter):
    entity_class = Bot
    child_entity_class = Worker
    signal_class = QalxBotSignal
    _user_only_methods = ['add']
    _bot_only_methods = ['replace_workers']

    def _unpacked_entities_to_valid_children(self, entity, unpacked_entities):
        """
        The unpacked entities are just a list on a Bot, therefore
        just return them

        :param entity: The Bot entity
        :param unpacked_entities: The unpacked Worker entities
        :return: The unpacked Worker entities
        """
        return unpacked_entities

    def _child_list_response(self, child_adapter, entity, **kwargs):
        """
        A bot needs to pass itself through to the child adapter in order
        to correctly build the list endpoint for Worker.  We also don't
        filter the workers by anything - we always return all of them for
        the given bot

        :param child_adapter: The child_adapter
        :param entity: The `QalxBot` entity
        :return: The child_adapter list response
        """
        return child_adapter.list(list_endpoint_kwargs={'bot_entity': entity})

    def add(self, name, **kwargs):
        """
        Creates a `Bot` instance.

        :param name: The name that this bot will be given
        :type name: str
        :param config: The bots config
        :type config: dict
        :param kwargs: Any data we want to use to create the bot
        :return: The newly created `Bot` instance
        """
        return super(QalxBot, self).add(host=self.session._host_info,
                                        name=name,
                                        **kwargs)

    def update_status(self, entity, status):
        """
        Updates the bots status

        :param entity: The entity that we are updating
        :param status: The status we want to update
        :return: None
        """
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid)
        logger.debug(f"update status{self.entity_class.entity_type} with guid {guid} with {endpoint}")
        self._process_api_request('patch', endpoint, status=status)

    def replace_workers(self, bot_entity, workers):
        """
        Completely replaces any Workers on the given bot.  Will return the
        replaced workers in an unpacked state

        :param bot_entity: The ~entities.bot.Bot entity that we are changing
        :param workers: The number of workers that we want this bot to have
        :return: A ~entities.bot.Bot instance with the updated workers
        """
        guid = bot_entity['guid']
        detail_endpoint = self.detail_endpoint(guid=guid)
        endpoint = f'{detail_endpoint}/replace-workers'
        logger.debug(f"replace workers {self.entity_class.entity_type} with guid {guid} with {endpoint}")

        entity = self._process_api_request('patch',
                                           endpoint,
                                           workers=workers)
        entity = self.entity_class(entity)
        entity = self._attempt_unpack(entity)
        return entity


class QalxWorker(QalxSignalAdapter):
    entity_class = Worker
    signal_class = QalxWorkerSignal

    @classmethod
    def list_endpoint(cls, *args, **kwargs):
        bot_entity = kwargs.get('bot_entity', None)
        bot_endpoint = QalxBot.detail_endpoint(guid=bot_entity['guid'])
        return f'{bot_endpoint}/{cls.entity_class.entity_type}'

    @classmethod
    def detail_endpoint(cls, guid, *args, **kwargs):
        bot_entity = kwargs.get('bot_entity', None)
        bot_endpoint = cls.list_endpoint(bot_entity=bot_entity)
        return f'{bot_endpoint}/{guid}'

    def get(self, guid, *args, **kwargs):
        """
        We completely override this as we don't want to send the `bot_entity`
        kwarg through to the `get` endpoint
        """
        bot_entity = kwargs.pop('bot_entity', None)
        endpoint = self.detail_endpoint(guid=guid, bot_entity=bot_entity)
        logger.debug(f"get {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        resp = self._process_api_request('get', endpoint, *args, **kwargs)
        return self.entity_class(resp)

    def reload(self, entity, **kwargs):
        """
        Reloads the current entity from the API

        :param bot: An instance of ~entities.bot.Bot
        :param entity: An instance of ~entities.worker.Worker
        :return: A refreshed instance of `self.entity`
        """
        bot_entity = kwargs.get('bot_entity', None)
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid, bot_entity=bot_entity)
        logger.debug(f"reload {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        worker_data = self._process_api_request('get', endpoint)
        return self.entity_class(worker_data)

    def update_status(self, bot_entity, entity, status):
        """
        Updates the workers status

        :param bot_entity: An instance of ~entities.bot.Bot
        :param entity: An instance of ~entities.worker.Worker
        :param status: The status we want to update
        :return: None
        """
        guid = entity['guid']
        endpoint = self.detail_endpoint(guid=guid, bot_entity=bot_entity)
        logger.debug(f"update status {self.entity_class.entity_type} with guid {guid} with {endpoint}")
        self._process_api_request('patch', endpoint, status=status)


class QalxSession:

    def __init__(self,
                 profile_name="default",
                 config_class=None,
                 skip_ini=False,
                 rest_api_class=None):
        """The session that any interaction with the API will use.
        Typically this won't get called directly but it gets passed to
        `QalxAdapter` instances to use for the duration of the `QalxAdapter`
        session

        :param profile_name: profile name to get from `config_class` (default="default")
        :type profile_name: basestring
        :param config_class: The class for the config we want to use for this session
        :param skip_ini: Should we skip loading the config from the inifile
        :type skip_ini: bool
        :param rest_api_class: The class to use for the rest api
        :ivar config: an instance of the `config_class` (default=pyqalx.config.UserConfig())
        """
        if config_class is None:
            config_class = UserConfig
        self.config = config_class()


        if not skip_ini:
            self.config.from_inifile(profile_name)

        configure_logging(self.config)
        if rest_api_class is None:
            rest_api_class = PyQalxAPI
        self.rest_api = rest_api_class(self.config)

    @property
    def log(self):
        return getLogger('pyqalx.integration')

    def _update_config(self, config):
        """
        Method to use if the config needs to be updated after the session has
        been created.  Used when creating a `~bot.Bot` as we need to create
        a `QalxSession` using a `BotConfig` and then update it with the token
        the `~bot.Bot` needs to use to interact with the `~entities.Queue`.
        Also updates the rest_api with the updated config

        :param config:
        :return:
        """
        self.config.update(config)
        self.rest_api = self.rest_api.__class__(self.config)

    @property
    def _host_info(self):
        return {
            "node": platform.node(),
            "platform": platform.platform(),
            # TODO: add more platform and IP address infos
        }

    @property
    def item(self):
        """
        returns a QalxItem adapter for this session

        :return: pyqalx.core.adapters.QalxItem
        """
        return QalxItem(self)

    @property
    def set(self):
        """
        returns a QalxSet adapter for this session

        :return: pyqalx.core.adapters.QalxSet
        """
        return QalxSet(self)

    @property
    def group(self):
        """
        returns a QalxGroup adapter for this session

        :return: pyqalx.core.adapters.QalxGroup
        """
        return QalxGroup(self)

    @property
    def queue(self):
        """
        returns a QalxQueue adapter for this session

        :return: pyqalx.core.adapters.QalxQueue
        """
        return QalxQueue(self)

    @property
    def bot(self):
        """
        returns a QalxBot adapter for this session

        :return: pyqalx.core.adapters.QalxBot
        """
        return QalxBot(self)

    @property
    def worker(self):
        """
        returns a QalxWorker adapter for this session

        :return: pyqalx.core.adapters.QalxWorker
        """
        return QalxWorker(self)
