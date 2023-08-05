import os
import uuid
from random import randint
from unittest.mock import call
from uuid import uuid4
import pytest

from pyqalx import QalxBot
from pyqalx.bot import Worker
from pyqalx.config import BotConfig
from pyqalx.transport.core import BasePyQalxAPI, \
    PyQalxAPIException
from pyqalx.transport.core import BasePyQalxAPI
from pyqalx.config import BotConfig, UserConfig
from pyqalx.core.adapters import QalxAdapter
from pyqalx.core.entities import Bot, Item, Queue, Set, Group, QalxListEntity
from pyqalx.core.entities.worker import Worker
from pyqalx.core.errors import QalxError, QalxAPIResponseError, \
    QalxMultipleEntityReturned, QalxFileError, QalxEntityNotFound, \
    QalxConfigError, QalxInvalidSession
from pyqalx.core.errors import  QalxEntityNotFound


@pytest.mark.parametrize("request_type", ['get', 'post', 'patch', 'delete'])
@pytest.mark.parametrize("endpoint", ['item', 'set', 'group', 'queue'])
@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_process_api_request(qalx_session, mocker, request_type, endpoint, entity_type):
    qalx_adapter = getattr(qalx_session, entity_type)
    mock_transport_function = mocker.patch("pyqalx.core.adapters.PyQalxAPI." + request_type)
    mock_transport_function.return_value = (True, {"guid": uuid4()})
    qalx_adapter._process_api_request(request_type, endpoint, thing="stuff")
    mock_transport_function.assert_called_once_with(endpoint, json={"meta": {},
                                                                    "thing": "stuff"})


@pytest.mark.parametrize("entity_type", ['item', 'queue'])
def test_get(qalx_session, mocker, entity_type):
    guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.return_value = {"guid": guid}
    qalx_adapter = getattr(qalx_session, entity_type)
    entity = qalx_adapter.get(guid=guid)
    assert entity['guid'] == guid
    endpoint = f"{entity_type}/{guid}"

    mocked_process_api_request.assert_called_with('get', endpoint)


def test_get_bot(qalx_session, mocker):
    """
    Tests that getting the bot correctly unpacks the workers
    """
    guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    worker = {'guid': uuid4().hex, 'meta': {'some': 'data'}}
    mocked_process_api_request.side_effect = [
        {"guid": guid,
         'workers': [worker['guid']]},
        {'data': [worker],
         'query': {'next': None}}
    ]
    qalx_adapter = QalxAdapter(entity_type=Bot.entity_type,
                               session=qalx_session)
    entity = qalx_adapter.get(guid=guid)

    expected_entity = {
        "guid": guid,
        "workers": [worker]
    }
    assert entity == expected_entity
    assert entity['guid'] == guid
    endpoint = f"{Bot.entity_type}/{guid}"

    mocked_process_api_request.assert_has_calls([
        call('get', endpoint),
        call('get', f'bot/{guid}/worker',
             limit=25,
             skip=0, sort=None)
    ])


def test_get_worker(qalx_session, mocker):
    """
    Tests that getting the worker correctly calls the endpoint.  We
    don't pass the bot_entity through to the `get` endpoint
    """
    guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    worker = {'guid': uuid4().hex, 'meta': {'some': 'data'}}
    mocked_process_api_request.return_value = worker

    entity = qalx_session.worker.get(guid=worker['guid'],
                                     bot_entity={'guid': guid})
    assert entity == worker

    mocked_process_api_request.assert_called_once_with('get',
                                                       f'bot/{guid}/worker/{worker["guid"]}')


def test_get_unpackable_set(qalx_session, mocker):
    """
    Tests the get call for a Set.  Also tests that we do multiple requests
    if there are a lot of items.
    """
    itemset_guid = uuid4().hex
    items = {}
    item_objects = {}
    chunk_1_page_1_data = []
    chunk_1_page_2_data = []
    chunk_2_page_1_data = []
    chunk_2_page_2_data = []
    for x in range(1, 198):
        # The `list` endpoint paginates the result but we also chunk the
        # request up to prevent hitting the max request size
        item_guid = uuid4().hex
        item = {'guid': item_guid, 'data': f'data{x}'}
        item_objects[f'item{x}'] = item
        items.update({f'item{x}': item_guid})
        if x <= 50:
            chunk_1_page_1_data.append(item)
        elif x <= 100:
            chunk_1_page_2_data.append(item)
        elif x <= 150:
            chunk_2_page_1_data.append(item)
        else:
            chunk_2_page_2_data.append(item)
    itemset = {"guid": itemset_guid, 'items': items}
    expected_itemset = {"guid": itemset_guid, 'items': item_objects}
    mocked_process_api_request = \
        mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    chunk_1_guid = f'in=({",".join([x["guid"] for x in chunk_1_page_1_data + chunk_1_page_2_data])})'
    chunk_1_page_1 = {'data': chunk_1_page_1_data,
                      'query': {'next': '<url-to-next-page-chunk-1>',}}
    chunk_1_page_2 = {'data': chunk_1_page_2_data,
                      'query': {'next': None}}
    chunk_2_guid = f'in=({",".join([x["guid"] for x in chunk_2_page_1_data + chunk_2_page_2_data])})'
    chunk_2_page_1 = {'data': chunk_2_page_1_data,
                      'query': {'next': '<url-to-next-page-chunk-2>', }}
    chunk_2_page_2 = {'data': chunk_2_page_2_data,
                      'query': {'next': None}}
    mocked_process_api_request.side_effect = [
        itemset,
        chunk_1_page_1,
        chunk_1_page_2,
        chunk_2_page_1,
        chunk_2_page_2,
    ]
    entity = qalx_session.set.get(guid=itemset_guid)

    assert entity == expected_itemset

    mocked_process_api_request.assert_has_calls([
        call('get', f'set/{itemset_guid}'),
        call('get', 'item', guid=chunk_1_guid, limit=25, skip=0, sort=None),
        call('get', chunk_1_page_1['query']['next']),
        call('get', 'item', guid=chunk_2_guid, limit=25, skip=0, sort=None),
        call('get', chunk_2_page_1['query']['next']),
    ])


def test_get_unpackable_group(qalx_session, mocker):
    """
    Tests the get call for a Group
    """
    guid = uuid4().hex
    item_guid = uuid4().hex
    item = {"guid": item_guid,
            'data': {'item': 'data'}}
    set_guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.side_effect = [
        {"guid": guid, 'sets': {'set1': set_guid}},
        {'data': [{"guid": set_guid, 'items': {'item1': item_guid}}],
         'query': {'next': None}
         },
        {'data': [item], 'query': {'next': None}}
    ]

    entity = qalx_session.group.get(guid=guid)

    assert entity['guid'] == guid

    assert entity == Group({
        'guid': guid,
        'sets': {'set1': {'guid': set_guid, 'items': {'item1': item}}}
    })
    mocked_process_api_request.assert_has_calls([
        call('get', f'group/{guid}'),
        call('get', 'set', guid=f'in=({set_guid})',
             limit=25, skip=0, sort=None),
        call('get', 'item', guid=f'in=({item_guid})',
             limit=25, skip=0, sort=None)
    ])


@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_archive_entity_by_guid(qalx_session, mocker, entity_type):
    guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.return_value = {"guid": guid, "info": {"archived": True}}
    qalx_adapter = getattr(qalx_session, entity_type)
    entity = qalx_adapter.entity_class({'guid': guid})
    archived_entity = qalx_adapter.archive(entity=entity)
    assert archived_entity['guid'] == guid
    endpoint = f"{entity_type}/{guid}/archive"
    mocked_process_api_request.assert_called_with('patch', endpoint)


@pytest.mark.parametrize("entity_type", ['item', 'queue'])
def test_reload(qalx_session, mocker, entity_type):
    guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.return_value = {"guid": guid, "meta": {"reloaded": True}}

    qalx_adapter = getattr(qalx_session, entity_type)
    original_entity = qalx_adapter.entity_class({"guid": guid,
                                                 "meta": {"reloaded": False}})
    entity = original_entity
    reloaded_entity = qalx_adapter.reload(entity=entity)
    assert reloaded_entity['meta']['reloaded']
    endpoint = f"{entity_type}/{guid}"
    mocked_process_api_request.assert_called_with('get', endpoint)


def test_reload_bot(qalx_session, mocker):
    guid = uuid4().hex
    worker = {'guid': uuid4().hex}
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.side_effect = [
        {"guid": guid, "workers": [worker['guid']], "meta": {"reloaded": True}},
        {'data': [worker],
         'query': {'next': None}}
    ]

    qalx_adapter = QalxAdapter(entity_type=Bot.entity_type,
                               session=qalx_session)
    original_entity = qalx_adapter.entity_class({"guid": guid,
                                                 "meta": {"reloaded": False}})
    entity = original_entity
    reloaded_entity = qalx_adapter.reload(entity=entity)
    assert reloaded_entity['meta']['reloaded']
    endpoint = f"{Bot.entity_type}/{guid}"

    mocked_process_api_request.assert_has_calls([
        call('get', endpoint),
        call('get', f'bot/{guid}/worker', limit=25, skip=0, sort=None)
    ])


def test_reload_unpackable_set(qalx_session, mocker):
    guid = uuid4().hex
    item_guid = uuid4().hex
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.side_effect = [
        {"guid": guid,
         "meta": {"reloaded": True},
         'items': {'item': item_guid}},
        {'data': [{'guid': item_guid, 'data': 'data'}],
         'query': {'next': None}}
    ]
    original_entity = Set({"guid": guid,
                           "meta": {"reloaded": False},
                           'items': {'item': item_guid}})

    reloaded_entity = qalx_session.set.reload(entity=original_entity)
    assert reloaded_entity['meta']['reloaded']

    mocked_process_api_request.assert_has_calls([
        call('get', f'set/{guid}'),
        call('get', 'item', guid=f'in=({item_guid})',
             limit=25, skip=0, sort=None)
    ])


def test_reload_unpackable_group(qalx_session, mocker):
    guid = uuid4().hex
    set_guid = uuid4().hex
    item_guid = uuid4().hex
    item = {"guid": item_guid,
            'data': {'item': 'data'}}
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    mocked_process_api_request.side_effect = [{"guid": guid, 'sets': {'set1': set_guid}},
                                              {'data': [{"guid": set_guid,
                                                         'items': {'item1': item_guid}}],
                                               'query': {'next': None}},
                                              {'data': [item],
                                               'query': {'next': None}}
                                              ]
    group_entity = Group({
        'guid': guid,
        'sets': {'set1': {'guid': set_guid, 'items': {'item1': item}}}
    })

    entity = qalx_session.group.reload(entity=group_entity)
    assert entity['guid'] == guid

    assert entity == group_entity
    mocked_process_api_request.assert_has_calls([
        call('get', f'group/{guid}'),
        call('get', 'set', guid=f'in=({set_guid})',
             limit=25, skip=0, sort=None),
        call('get', 'item', guid=f'in=({item_guid})',
             limit=25, skip=0, sort=None)
    ])


@pytest.mark.parametrize("entity_type", ['item', 'queue'])
def test_save(qalx_session, mocker, entity_type):
    qalx_adapter = getattr(qalx_session, entity_type)
    Entity = qalx_adapter.entity_class
    guid = uuid4()
    entity_structure = {"guid": guid, "info": {"archived": False}, "data": {"thing": "stuff"}}

    entity = Entity(entity_structure)
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    endpoint = f"{entity_type}/{guid}"
    mocked_process_api_request.return_value(entity_structure)

    qalx_adapter.save(entity=entity)
    mocked_process_api_request.assert_called_with('patch', endpoint, data=entity_structure['data'])


def test_save_unpacked_set(qalx_session, mocker):
    guid = uuid4()
    unpacked_items = {
        "item1": Item({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data1"}}),
        "item2": Item({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data2"}}),
        "item3": Item({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data3"}}),
    }
    item4 = Item({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data4"}})
    unpacked_entity = {"guid": guid, "info": {"archived": False}, 'items': unpacked_items}
    entity = Set(unpacked_entity)
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    entity['items']['item4'] = item4

    saved_entity = qalx_session.set.save(entity=entity)
    mocked_process_api_request.assert_called_with('patch', f'set/{guid}',
                                                  items={k: str(v['guid']) for k, v in entity['items'].items()})
    assert saved_entity['items'] == unpacked_items, 'Set not unpacked'


def test_save_unpacked_group(qalx_session, mocker):
    guid = uuid4()
    unpacked_sets = {
        "set1": Set({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data1"}}),
        "set2": Set({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data2"}}),
        "set3": Set({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data3"}}),
    }
    set4 = Set({"guid": uuid4(), "info": {"archived": False}, "data": {"some": "data4"}})
    unpacked_entity = {"guid": guid, "info": {"archived": False}, 'sets': unpacked_sets}
    entity = Group(unpacked_entity)
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    entity['sets']['set4'] = set4
    # This also tests that we can call a specific adapter
    saved_entity = qalx_session.group.save(entity=entity)
    mocked_process_api_request.assert_called_with('patch', f'group/{guid}',
                                                  sets={k: str(v['guid']) for k, v in entity['sets'].items()})
    assert saved_entity['sets'] == unpacked_sets, 'Group not unpacked'


def test_add(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    guid = uuid4()
    item_structure = {"guid": guid, "info": {"archived": False}, "data": {"thing": "stuff"}}
    mocked_process_api_request.return_value = item_structure
    # TODO: maybe call this for each entity_type?????
    qalx_adapter = qalx_session.item
    item1 = qalx_adapter.add(data=item_structure['data'])
    mocked_process_api_request.assert_called_with('post', 'item', data=item_structure['data'])
    assert isinstance(item1, Item)
    meta = {"some": "meta data"}
    item2 = qalx_adapter.add(data=item_structure['data'], meta=meta)
    mocked_process_api_request.assert_called_with('post', 'item', data=item_structure['data'], meta=meta)
    assert isinstance(item2, Item)


def test_add_item_file(qalx_session, mocker):
    file_location = os.path.abspath(__file__)
    file_content = open(file_location, "rb").read()
    qalx_adapter = qalx_session.item
    mocked_build_request = mocker.patch.object(BasePyQalxAPI, '_build_request')
    mocked_build_request.return_value = (True, {"file":{"put_url": "some_url"}})
    item1 = qalx_adapter.add_file(input_file=file_location)
    mocked_build_request.assert_called_with(url='some_url',
                                            include_auth_headers=False,
                                            method='PUT',
                                            data=file_content)
    assert isinstance(item1, Item)


def test_add_item_file_with_filepath_and_filename(qalx_session, mocker):
    file_location = os.path.abspath(__file__)
    file_name = file_location.split("/")[-1]
    file_content = open(file_location, "rb").read()
    qalx_adapter = qalx_session.item
    mocked_build_request = mocker.patch.object(BasePyQalxAPI, '_build_request')
    mocked_build_request.return_value = (True, {"file":{"put_url": "some_url"}})
    item1 = qalx_adapter.add_file(input_file=file_location, file_name=file_name)
    mocked_build_request.assert_called_with(url='some_url',
                                            include_auth_headers=False,
                                            method='PUT',
                                            data=file_content)
    assert isinstance(item1, Item)


def test_add_item_file_with_filestream_and_filename(qalx_session, mocker):
    file_location = os.path.abspath(__file__)
    file_name = file_location.split("/")[-1]
    file_instance = open(file_location, "r")
    qalx_adapter = qalx_session.item
    mocked_build_request = mocker.patch.object(BasePyQalxAPI, '_build_request')
    mocked_build_request.return_value = (True, {"file": {"put_url": "some_url"}})
    test_item = qalx_adapter.add_file(input_file=file_instance, file_name=file_name)
    mocked_build_request.assert_called_with(url='some_url',
                                            include_auth_headers=False,
                                            method='PUT',
                                            data=file_instance)
    assert isinstance(test_item, Item)


def test_get_item_file(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    guid = uuid4().hex
    item_structure = {"guid": guid, "info": {"archived": False},
                      "file": {"url": "s3://thefile", "filename": "some_file.extension"}}
    mocked_process_api_request.return_value = item_structure
    item1 = qalx_session.item.get(guid=guid)
    mocked_process_api_request.assert_called_with('get', 'item/' + guid)
    mocked_requests = mocker.patch('pyqalx.core.entities.item.requests')
    assert isinstance(item1, Item)

    some_bytes = b'some bytes'
    mock_response = mocker.MagicMock()
    mocked_requests.get.return_value = mock_response
    mock_response.content = some_bytes
    mock_response.ok = True
    file_bytes = item1.read_file()
    mocked_requests.get.assert_called_with(url=item_structure['file']['url'])
    assert file_bytes == some_bytes
    fake_path = "/a/path/"
    mocked_open = mocker.mock_open()
    m = mocker.patch('pyqalx.core.entities.item.open', mocked_open, create=True)
    item1.save_file(fake_path)
    full_fake_path = os.path.join(fake_path, item_structure['file']['filename'])
    mocked_open.assert_called_with(full_fake_path, 'wb')


def test_add_set(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    guid1 = uuid4().hex
    guid2 = uuid4().hex
    item1_structure = {"guid": guid1, "info": {"archived": False}, "data": {"thing": "stuff"}}
    item2_structure = {"guid": guid2, "info": {"archived": False}, "data": {"thing": "stuff"}}
    mocked_process_api_request.return_value = {"guid": uuid4(), "info": {"some": "info"}, "items":
        {"item1": guid1, "item2": guid2}}
    itemset = qalx_session.set.add(items={
        "item1": Item(item1_structure), "item2": Item(item2_structure)
    })
    mocked_process_api_request.assert_called_with('post', 'set', items={"item1": guid1, "item2": guid2})
    assert isinstance(itemset, Set)
    assert itemset['items']


def test_add_group(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    guid1 = uuid4().hex
    guid2 = uuid4().hex
    set1_structure = {"guid": guid1, "info": {"archived": False},
                      "items": {"item1": "item_guid1", "item2": "item_guid2"}}
    set2_structure = {"guid": guid2, "info": {"archived": False},
                      "items": {"item3": "item_guid3", "item4": "item_guid4"}}
    mocked_process_api_request.return_value = {"guid": uuid4(), "info": {"some": "info"},
                                               "sets": {"set1": guid1, "set2": guid2}}
    group = qalx_session.group.add(sets={"set1": Set(set1_structure), "set2": Set(set2_structure)})
    mocked_process_api_request.assert_called_with('post', 'group', sets={"set1": guid1, "set2": guid2})
    assert isinstance(group, Group)


def test_add_queue(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    queue = qalx_session.queue.add(name="unittest queue", meta={"some": "stuff"})

    mocked_process_api_request.assert_called_with('post',
                                                  'queue',
                                                  name="unittest queue",
                                                  parameters=qalx_session.queue._queue_params,
                                                  meta={"some": "stuff"})
    assert isinstance(queue, Queue)

    queue = qalx_session.queue.add(name="unittest queue")
    mocked_process_api_request.assert_called_with('post',
                                                  'queue',
                                                  name="unittest queue",
                                                  parameters=qalx_session.queue._queue_params)
    assert isinstance(queue, Queue)


@pytest.mark.parametrize("entity_type", ['item', 'set', 'group', 'queue'])
def test_list_entities_guid_none_many_true(qalx_session, mocker, entity_type):
    """
    Tests that we can get multiple entities via querying the `list` endpoint
    when many=True
    """
    return_data = {'query': '<users search query>',
                   'sort': '<users sort query>',
                   'next': '<url-to-next-page>',
                   'previous': '<url-to-previous-page>',
                   'data': []}
    for x in range(0, 50):
        # Build the data we expect from the API
        return_data['data'].append({'guid': str(uuid.uuid4())})
    mocked_process_api_request = mocker.patch(
        'pyqalx.core.adapters.QalxAdapter._process_api_request',
        return_value=return_data)

    params = dict(sort=None, skip=randint(0, 100), limit=randint(1, 500))
    qalx_adapter = getattr(qalx_session, entity_type)
    entities = qalx_adapter.list(many=True, **params)
    assert isinstance(entities, QalxListEntity)

    for entity in entities['data']:
        assert isinstance(entity, qalx_adapter.entity_class)
    mocked_process_api_request.assert_called_with("get", entity_type, **params)


def test_get_queue_by_name(qalx_session, mocker):
    """
    Tests the get_queue_by_name method returns a full queue

    """
    return_data = {'query': '<users search query>',
                   'sort': '<users sort query>',
                   'next': '<url-to-next-page>',
                   'previous': '<url-to-previous-page>',
                   'data': [{'guid': str(uuid.uuid4())}]}
    api_method = mocker.patch.object(
        QalxAdapter, '_process_api_request',)
    api_method.side_effect = [
        return_data,
        return_data['data'][0]
    ]
    qalx_adapter = qalx_session.queue

    q = qalx_adapter.get_by_name("unittest queue")

    assert q == return_data['data'][0]

    api_method.assert_called_once_with('get',
                                       'queue',
                                       limit=25,
                                       name='unittest queue',
                                       skip=0,
                                       sort=None)


def test_get_or_create_queue(qalx_session, mocker):
    qalx_adapter = qalx_session.queue
    get_by_name_method = mocker.patch.object(qalx_adapter, 'get_by_name')
    get_by_name_method.return_value = Queue({"meta": {"name": "unittest queue"}})
    q = qalx_adapter.get_or_create("unittest queue")
    get_by_name_method.assert_called_with(name="unittest queue")
    assert isinstance(q, Queue)
    get_by_name_method = mocker.patch.object(qalx_adapter, 'get_by_name')
    get_by_name_method.side_effect = QalxEntityNotFound
    create_queue_method = mocker.patch.object(qalx_adapter, 'add')
    q = qalx_adapter.get_or_create("unittest new queue", meta={"some": "meta"})
    create_queue_method.assert_called_with("unittest new queue", meta={"some": "meta"})


def test_add_bot(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')

    class BotConfigWithExtra(BotConfig):
        @property
        def defaults(self):
            config = super(BotConfigWithExtra, self).defaults
            config.update({"Some": "config"})
            return config
    bot_config = BotConfigWithExtra()
    qalx_adapter = QalxAdapter(entity_type=Bot.entity_type,
                               session=qalx_session)
    bot = qalx_adapter.add(name='MyBot', config=bot_config)
    mocked_process_api_request.assert_called_with('post', 'bot',
                                                  name='MyBot',
                                                  config=bot_config,
                                                  host=qalx_adapter.session._host_info)


def test_update_bot_status(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    qalx_adapter = QalxAdapter(entity_type=Bot.entity_type,
                               session=qalx_session)
    entity = Bot({'guid': '1234'})
    bot = qalx_adapter.update_status(status="unittest",
                                     entity=entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234', status="unittest")


def test_send_signals_bot(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    qalx_bot_adapter = QalxBot(session=qalx_session)
    bot_entity = Bot({'guid': '1234'})
    qalx_bot_adapter.terminate(bot_entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234',
                                                  signal={"terminate": True,
                                                          "warm": True})
    qalx_bot_adapter.stop(bot_entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234',
                                                  signal={"stop": True})
    qalx_bot_adapter.resume(bot_entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234',
                                                  signal={"stop": False})


def test_send_signals_worker_term(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    bot_entity = Bot({'guid': '1234'})
    worker_entity = Worker({'guid': '66666'})

    qalx_session.worker.terminate(worker_entity, bot_entity=bot_entity, warm=True)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"terminate": True,
                                                          "warm": True})

    qalx_session.worker.terminate(worker_entity, bot_entity=bot_entity, warm=False)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"terminate": True,
                                                          "cold": True,
                                                          "requeue_job": False})

    qalx_session.worker.terminate(worker_entity, bot_entity=bot_entity,
                                  warm=False, requeue_job=False)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"terminate": True,
                                                          "cold": True,
                                                          "requeue_job": False})

    qalx_session.worker.terminate(worker_entity, bot_entity=bot_entity,
                                  warm=False, requeue_job=True)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"terminate": True,
                                                          "cold": True,
                                                          "requeue_job": True})


def test_send_signals_worker_stop(qalx_session, mocker):
    mocked_process_api_request = mocker.patch('pyqalx.core.adapters.QalxAdapter._process_api_request')
    bot_entity = Bot({'guid': '1234'})
    worker_entity = Worker({'guid': '66666'})
    qalx_session.worker.stop(worker_entity, bot_entity=bot_entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"stop": True})
    qalx_session.worker.resume(worker_entity, bot_entity=bot_entity)
    mocked_process_api_request.assert_called_with('patch', 'bot/1234/worker/66666',
                                                  signal={"stop": False})


@pytest.mark.parametrize("entity_type", ['item', 'queue'])
def test_list_many_false(qalx_session, mocker, entity_type):
    """
    Tests that the `get` method returns a single entity when querying a list
    endpoint
    """
    return_data = {'query': '<users search query>',
                   'sort': '<users sort query>',
                   'next': '<url-to-next-page>',
                   'previous': '<url-to-previous-page>',
                   'data': [{'guid': str(uuid.uuid4())},]}
    list_method = mocker.patch.object(
        QalxAdapter, '_process_api_request',
        return_value=return_data)
    qalx_adapter = getattr(qalx_session, entity_type)
    entity = qalx_adapter.list(many=False,
                               meta={'name': 'some name'})

    assert entity == return_data['data'][0]

    list_method.assert_called_once_with('get',
                                        entity_type,
                                        limit=25,
                                        meta={'name': 'some name'},
                                        skip=0,
                                        sort=None)


@pytest.mark.parametrize("entity_type", ['set'])
def test_list_many_false_set(qalx_session, mocker, entity_type):
    """
    Tests that the `list` method returns a single set when querying a list
    endpoint
    """
    itemset = {'guid': str(uuid.uuid4()),
               'items': {'test': str(uuid.uuid4()),
                         'test1': str(uuid.uuid4())}}
    list_data = {'query': '<users search query>',
                 'sort': '<users sort query>',
                 'next': '<url-to-next-page>',
                 'previous': '<url-to-previous-page>',
                 'data': [itemset, ]}
    get_data = {'data':
        [{'guid': list_data['data'][0]['items']['test'],
          'data': 'data stored here'},
         {'guid': list_data['data'][0]['items']['test1'],
          'data': 'data stored here'}
         ],
        'query': {'next': None}
    }
    api_method = mocker.patch.object(
        QalxAdapter, '_process_api_request')
    api_method.side_effect = [list_data,
                              get_data]
    qalx_adapter = getattr(qalx_session, entity_type)

    entity = qalx_adapter.list(many=False,
                               meta={'name': 'some name'})

    itemset['items']['test'] = get_data['data'][0]
    itemset['items']['test1'] = get_data['data'][1]

    assert entity == itemset
    list_call = call('get',
                     entity_type,
                     limit=25,
                     meta={'name': 'some name'},
                     skip=0,
                     sort=None)
    item_list_call = call('get',
                          f'item',
                          guid=f'in=({itemset["items"]["test"]["guid"]},'
                               f'{itemset["items"]["test1"]["guid"]})',
                          limit=25,
                          skip=0,
                          sort=None)
    api_method.assert_has_calls([list_call, item_list_call])


@pytest.mark.parametrize("entity_type", ['group'])
def test_list_many_false_group(qalx_session, mocker, entity_type):
    """
    Tests that the `list` method returns a single group when querying a list
    endpoint
    """
    item = {'data': [{'guid': str(uuid.uuid4()), 'data': 'stored here'}],
            'query': {'next': None},}
    itemset = {'data': [{'guid': str(uuid.uuid4()),
               'items': {'item1': item['data'][0]['guid']}}],
               'query': {'next': None},
               }
    itemset_group = {'guid': str(uuid.uuid4()),
                     'sets': {'set1': itemset['data'][0]['guid']}}
    list_data = {'query': '<users search query>',
                 'sort': '<users sort query>',
                 'next': '<url-to-next-page>',
                 'previous': '<url-to-previous-page>',
                 'data': [itemset_group, ]}
    api_method = mocker.patch.object(
        QalxAdapter, '_process_api_request')
    api_method.side_effect = [list_data,
                              itemset,
                              item]

    qalx_adapter = getattr(qalx_session, entity_type)

    entity = qalx_adapter.list(many=False,
                               meta={'name': 'some name'})
    set_entity = Set({
        'guid': itemset['data'][0]['guid'],
        'items': {'item1': Item(item['data'][0])},
    })
    group_entity = Group({
        'guid': itemset_group['guid'],
        'sets': {'set1': set_entity}
    })

    assert entity == group_entity
    list_call = call('get',
                     entity_type,
                     limit=25,
                     meta={'name': 'some name'},
                     skip=0,
                     sort=None)

    set_list_call = call('get',
                         f'set',
                         guid=f'in=({itemset_group["sets"]["set1"]})',
                         limit=25,
                         skip=0,
                         sort=None)

    item_list_call = call('get',
                          f'item',
                          guid=f'in=({itemset["data"][0]["items"]["item1"]})',
                          limit=25,
                          skip=0,
                          sort=None)
    api_method.assert_has_calls([list_call, set_list_call, item_list_call])


def test_bot_user_only(mocker, qalx_session, qalx_session_class,
                       bot_config_class, user_config_class):
    """
    Tests that a session with a UserConfig can add a Bot
    """
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')

    user_adapter = QalxAdapter(entity_type=Bot.entity_type,
                               session=qalx_session)
    user_adapter.add(name='MyBot', config={})
    assert mocked_api_request.called is True


def test_qalx_session_default_config_class(qalx_session_class,):
    """
    Tests that the QalxSession uses UserConfig if no config_class
    specified
    """
    session = qalx_session_class(skip_ini=True)
    assert isinstance(session.config, UserConfig) is True

