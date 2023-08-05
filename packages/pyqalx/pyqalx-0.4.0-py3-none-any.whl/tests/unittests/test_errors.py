import os
import uuid
from uuid import uuid4

import pytest

from pyqalx import QalxAdapter, QalxItem
from pyqalx.core.entities import Item, Queue, Bot
from pyqalx.core.errors import QalxInvalidSession, QalxEntityTypeNotFound, \
    QalxMultipleEntityReturned, QalxConfigError, QalxError, \
    QalxAPIResponseError, QalxNoGUIDError, QalxEntityNotFound, QalxFileError
from pyqalx.transport.core import PyQalxAPIException


def test_adapter_invalid_session_class():
    """
    Tests that the QalxAdapter raises a QalxInvalidSession if the session
    isn't an instance of QalxSession
    """
    with pytest.raises(QalxInvalidSession):
        QalxAdapter(session='INVALIDSESSION')


def test_adapter_no_entity_type_found(qalx_session):
    """
    Tests that the QalxAdapter raises a QalxEntityTypeNotFound if the
    entity type isn't found
    """
    with pytest.raises(QalxEntityTypeNotFound):
        QalxAdapter(session=qalx_session, entity_type='INVALID')


def test_adapter_multiple_entity_type_found(qalx_session):
    """
    Tests that the QalxAdapter raises a QalxMultipleEntityReturned if multiple
    of the same entity type are found
    """
    class DuplicateAdapter(QalxItem):
        # We can only have a single adapter per entity class.
        # Therefore, creating this one will raise an error
        entity_class = Item
    with pytest.raises(QalxMultipleEntityReturned):
        QalxAdapter(session=qalx_session, entity_type=Item.entity_type)


def test_adapter_getattribute_user_only_config_error(qalx_session_class,
                                                     bot_config_class):
    """
    Tests that the QalxAdapter raises a QalxConfigError if a `_user_only_method`
    if called in the context of a `BotConfig
    """
    bot_session = qalx_session_class(config_class=bot_config_class,
                                     skip_ini=True)
    adapter = QalxItem(session=bot_session)
    # Always force this to be `add` so it's repeatable for testing
    adapter._user_only_methods = ['add']
    with pytest.raises(QalxConfigError):
        adapter.add()


def test_adapter_getattribute_bot_only_config_error(qalx_session):
    """
    Tests that the QalxAdapter raises a QalxConfigError if a `_user_only_method`
    if called in the context of a `BotConfig
    """
    adapter = QalxItem(session=qalx_session)
    # Always force this to be `add` so it's repeatable for testing
    adapter._bot_only_methods = ['add']
    with pytest.raises(QalxConfigError):
        adapter.add()


@pytest.mark.parametrize("request_type", ['get', 'post', 'patch', 'delete'])
@pytest.mark.parametrize("endpoint", ['item', 'set', 'group', 'queue'])
@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_process_api_request_non_json_error(qalx_session, mocker, request_type, endpoint, entity_type):
    mocker.patch("pyqalx.core.adapters.PyQalxAPI." + request_type)
    with pytest.raises(QalxError):
        qalx_adapter = getattr(qalx_session, entity_type)
        qalx_adapter._process_api_request(request_type, endpoint, thing=uuid4())


def test_adapter_process_api_request_invalid_method(qalx_session):
    """
    Tests that a QalxError is raised if the method isn't valid
    """
    with pytest.raises(QalxError):
        qalx_session.item._process_api_request(method='INVALID')


@pytest.mark.parametrize("request_type", ['get', 'post', 'patch', 'delete'])
@pytest.mark.parametrize("endpoint", ['item', 'set', 'group', 'queue'])
@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_process_api_request_http_error(qalx_session, mocker, request_type, endpoint, entity_type):
    mock_transport_function = mocker.patch("pyqalx.core.adapters.PyQalxAPI." + request_type)
    mock_transport_function.return_value = (False, {"I'm a": "complete HTTP failure"})
    with pytest.raises(QalxAPIResponseError) as e:
        qalx_adapter = getattr(qalx_session, entity_type)
        qalx_adapter._process_api_request(request_type, endpoint, thing="stuff")
        assert "I'm a: complete HTTP failure" in str(e)


@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_list_error_multiple(qalx_session, mocker, entity_type):
    """
    Tests that a QalxMultipleEntitiesReturned is raised if we list with
    many=False and get multiple entities returned
    """
    return_data = {'query': '<users search query>',
                   'sort': '<users sort query>',
                   'next': '<url-to-next-page>',
                   'previous': '<url-to-previous-page>',
                   'data': [{'guid': str(uuid.uuid4())},
                            {'guid': str(uuid.uuid4())}]}
    list_method = mocker.patch.object(
        QalxAdapter, '_process_api_request',
        return_value=return_data)
    qalx_adapter = getattr(qalx_session, entity_type)
    with pytest.raises(QalxMultipleEntityReturned):
        qalx_adapter.list(many=False,
                          meta={'name': 'some name'})
    list_method.assert_called_once_with('get',
                                        entity_type,
                                        limit=25,
                                        meta={'name': 'some name'},
                                        skip=0,
                                        sort=None)


@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_list_many_false_none_found(qalx_session, mocker, entity_type):
    """
    Tests that a QalxEntityNotFound is raised if we list with
    many=False and get multiple entities returned
    """
    return_data = {'query': '<users search query>',
                   'sort': '<users sort query>',
                   'next': '<url-to-next-page>',
                   'previous': '<url-to-previous-page>',
                   'data': []}
    list_method = mocker.patch.object(
        QalxAdapter, '_process_api_request',
        return_value=return_data)
    qalx_adapter = getattr(qalx_session, entity_type)
    with pytest.raises(QalxEntityNotFound):
        qalx_adapter.list(many=False,
                          meta={'name': 'some name'}, )
    list_method.assert_called_once_with('get',
                                        entity_type,
                                        limit=25,
                                        meta={'name': 'some name'},
                                        skip=0,
                                        sort=None)


def test_adapter_save_no_guid(qalx_session):
    """
    Tests that if we call save with an entity without a guid that a
    QalxNoGUIDError is raised
    """
    with pytest.raises(QalxNoGUIDError):
        qalx_session.item.save(entity={'no': 'guid'})


def test_adapter_get_child_entities_kids_not_list_or_dict(qalx_session):
    """
    Tests that a QalxError is raised if the `self.kids` key on
    an entity does not resolve to a dict or a list
    """
    kids = qalx_session.set.kids
    for possible_type in ['invalid', True, 25]:
        # Iterate through possible invalid types to ensure the exception is
        # raised
        with pytest.raises(QalxError):
            qalx_session.set._get_child_entities(entity={kids: possible_type})


def test_adapter_add_item_data_not_dict(qalx_session):
    """
    Tests that a QalxError is raised if an item is added and the data
    isn't in `dict` format
    """
    for possible_type in ['invalid', True, 25, ['list', 'of', 'data']]:
        # Iterate through possible invalid types to ensure the exception is
        # raised
        with pytest.raises(QalxError):
            qalx_session.item.add(data=possible_type)


def test_adapter_add_item_file_no_file_name_stream(qalx_session):
    """
    Tests that a QalxFileError is raised if we are adding a file using
    a file stream without specifying a file name
    """
    with pytest.raises(QalxFileError):
        fs = open(os.path.abspath(__file__), 'rb')
        qalx_session.item.add_file(input_file=fs)


def test_transport_add_item_file_no_filename_and_filepath(qalx_session):
    """
    Tests that a PyQalxAPIException is raised if we try to add an
    item with not filename or file path
    """
    qalx_adapter = qalx_session.item
    with pytest.raises(PyQalxAPIException):
        qalx_adapter.add_file(file_name="", input_file="")


def test_get_queue_messages(qalx_session):
    """
    Tests that a QalxConfigError is raised if the config on the session isn't
    a bot config that the user cannot get messages from the queue
    """
    with pytest.raises(QalxConfigError):
        # Just create a fake ~queue.Queue instance for the entity
        entity = Queue({})
        qalx_session.queue.get_messages(queue=entity)


def test_bot_user_only(mocker, qalx_session, qalx_session_class,
                       bot_config_class, user_config_class):
    """
    Tests that a QalxConfigError is raised if a session with a BotConfig
    attempts to add a bot
    """
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')
    bot_session = qalx_session_class(config_class=bot_config_class,
                                     skip_ini=True)
    bot_adapter = QalxAdapter(entity_type=Bot.entity_type,
                              session=bot_session)

    with pytest.raises(QalxConfigError):
        bot_adapter.add(name='MyBot', config={})
        assert mocked_api_request.called is False
