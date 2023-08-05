"""tests for bots

.. note::

    These tests are all marked as `xfail` as the changes to Bots and Workers make them very brittle.
    Functional tests will provide coverage in the short term. Aim is to remove or re-write these long-term


"""
import copy
import json
from multiprocessing import Manager

import pytest

from pyqalx import Bot
from pyqalx.config import BotConfig, UserConfig
from pyqalx.core.adapters import QalxAdapter, QalxSession
from pyqalx.core.entities.queue import QueueMessage
from tests.model_entities import queue_response, entities_response, bot_post, \
    replace_workers_post, workers


def bot_processes(bot, jobs, expected_output):
    """
    Helper function for handling the bot processes
    :param bot: The bot instance
    :param jobs: An instance of Manager().list().  Used to keep track of all
                 the jobs across multiple processes
    :param expected_output: An instance of Manager().list().  Used to keep
                            track of all outputs for the jobs across multiple
                            processes
    :return: bot, jobs, expected_output
    """
    @bot.initialisation
    def _initialisation(user_qalx):
        jobs.append('init_complete')
        return True

    @bot.begin
    def _begin(_job):
        val = "begin"

        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.preload
    def _preload(_job):
        val = 'preload'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.onload
    def _onload(_job):
        val = 'onload'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.preprocess
    def _preprocess(_job):
        val = 'preprocess'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.process
    def _process(_job):
        val = 'process'
        step_result = {"test": val}
        if _job.entity.get('items') is not None:
            step_result['items'] = _job.entity['items']
        if _job.entity.get('sets') is not None:
            step_result['sets'] = _job.entity['sets']
        _job.add_step_result(True, step_result)
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.precompletion
    def _precompletion(_job):
        val = 'precompletion'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.postprocess
    def _postprocess(_job):
        val = 'postprocess'
        _job.add_step_result(True, {"test": val})
        _job.stop = True
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.ontermination
    def _ontermination(_job):
        val = 'termination'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)

    @bot.onwait
    def _onwait(_job):
        val = 'onwait'
        _job.add_step_result(True, {"test": val})
        jobs.append(_job.last_step_result)
        expected_output.append(val)
    return bot, jobs, expected_output


@pytest.mark.xfail
def test_bot_runs_all_functions(mocker, qalx_session,
                                bot_config_class, user_config_class):
    """
    Tests that a bot runs through all the expected functions and processes
    them accordingly
    """
    mocker.patch.object(QueueMessage, '_do_heartbeat')
    # No response from status update
    status_update = {}
    get_queues = {
        'data': [queue_response],
    }

    get_item = entities_response['item'][0]
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')
    workers_list_response = {'data': [workers[0], workers[1]],
                             'query': {'next': None}}
    mocked_api_request.side_effect = [
        # The first call creates a bot
        bot_post,
        replace_workers_post,
        workers_list_response,
        status_update,
        get_queues,
        queue_response,
        entities_response['item'][0],
    ]
    mocked_boto3 = mocker.patch('pyqalx.core.entities.queue.boto3')
    mocked_boto3.client.return_value.receive_message.side_effect = [
        {'Messages': [{'Body': json.dumps({
            'entity_type': 'item',
            'entity_guid': get_item['guid']
        }),
            'ReceiptHandle': 'receipt handle'}]}
    ]

    bot = Bot(bot_name='test_bot',
              queue_name='test_queue',
              skip_ini=True,
              qalx_session_class=qalx_session.__class__,
              user_config_class=user_config_class,
              bot_config_class=bot_config_class)

    with Manager() as manager:
        # Use a manager for a shared state across all processes
        jobs = manager.list()
        expected_output = manager.list()

        bot, jobs, expected_output = bot_processes(bot, jobs, expected_output)

        bot.start(processes=1)
        assert jobs[0] == 'init_complete'

        for cnt, job in enumerate(jobs[1:]):
            assert job.result_data == {'test': expected_output[cnt]}
            # This test case should never wait
            assert job.result_data != {'test': 'onwait'}, \
                "BotProcess called `onwait` function when it shouldn't have"


@pytest.mark.slow
@pytest.mark.xfail
def test_bot_runs_all_functions_wait_response(mocker, qalx_session,
                                              bot_config_class,
                                              user_config_class):
    """
    Tests that a bot runs through all the expected functions and processes
    them accordingly.  This also tests that the wait response works in case
    we don't get a message from SQS.
    This will take a while to complete due to the
    `sleep(wait_time * spread_factor)`
    """
    mocker.patch.object(QueueMessage, '_do_heartbeat')
    # No response from status update
    status_update = {}
    get_queues = {
        'data': [queue_response],
    }

    get_item = entities_response['item'][0]
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')

    updated_replace_workers_post = copy.deepcopy(replace_workers_post)
    # We are only testing with a single worker
    updated_replace_workers_post['workers'].pop()
    workers_list_response = {'data': [workers[0]],
                             'query': {'next': None}}
    mocked_api_request.side_effect = [
        # The first call creates a bot
        bot_post,
        updated_replace_workers_post,
        workers_list_response,
        status_update,
        get_queues,
        queue_response,
        entities_response['item'][0],
    ]
    mocked_boto3 = mocker.patch('pyqalx.core.entities.queue.boto3')
    mocked_boto3.client.return_value.receive_message.side_effect = [
        {},
        {'Messages': [{'Body': json.dumps({
            'entity_type': 'item',
            'entity_guid': get_item['guid']
        }),
            'ReceiptHandle': 'receipt handle'}]}
    ]

    bot = Bot(bot_name='test_bot',
              queue_name='test_queue',
              skip_ini=True,
              qalx_session_class=qalx_session.__class__,
              user_config_class=user_config_class,
              bot_config_class=bot_config_class)

    with Manager() as manager:
        # Use a manager for a shared state across all processes
        jobs = manager.list()
        expected_output = manager.list()

        bot, jobs, expected_output = bot_processes(bot, jobs, expected_output)

        bot.start(processes=1)
        assert jobs[0] == 'init_complete'

        for cnt, job in enumerate(jobs[1:]):
            assert job.result_data == {'test': expected_output[cnt]}


@pytest.mark.slow
@pytest.mark.xfail
def test_bot_runs_all_functions_kill_after(mocker, qalx_session,
                                           bot_config_class, user_config_class):
    """
    Tests that a bot runs through all the expected functions and processes
    them accordingly - killing the process if we have attempted to get messages
    more than `KILL_AFTER` times.  This also tests reading from the ini file.
    This will take a while to complete due to the
    `sleep(wait_time * spread_factor)`
    """
    mocker.patch.object(QueueMessage, '_do_heartbeat')
    # No response from status update
    status_update = {}
    get_queues = {
        'data': [queue_response],
    }

    get_item = entities_response['item'][0]
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')
    updated_replace_workers_post = copy.deepcopy(replace_workers_post)
    # We are only testing with a single worker
    updated_replace_workers_post['workers'].pop()
    workers_list_response = {'data': [workers[0]],
                             'query': {'next': None}}
    mocked_api_request.side_effect = [
        # The first call creates a bot
        bot_post,
        updated_replace_workers_post,
        workers_list_response,
        status_update,
        get_queues,
        queue_response,
        entities_response['item'][0],
    ]
    mocked_boto3 = mocker.patch('pyqalx.core.entities.queue.boto3')
    mocked_boto3.client.return_value.receive_message.side_effect = [
        # This is key to the `KILL_AFTER` test.  We will kill after two
        # attempts.  Meaning that the actual message will never get read
        {},
        {},
        # This will never get read
        {'Messages': [{'Body': json.dumps({
            'entity_type': 'item',
            'entity_guid': get_item['guid']
        }),
            'ReceiptHandle': 'receipt handle'}]}
    ]
    # Mock the config file that is normally stored on the filesystem
    mocked_path = mocker.patch('pyqalx.config.os.path.exists')
    mocked_path.return_value = True
    mo = mocker.mock_open(read_data="[default]\nKILL_AFTER=2")
    mocker.patch('pyqalx.config.open', mo)

    bot = Bot(bot_name='test_bot',
              queue_name='test_queue',
              skip_ini=False,
              user_config_class=user_config_class,
              qalx_session_class=qalx_session.__class__,
              bot_config_class=bot_config_class)

    with Manager() as manager:
        # Use a manager for a shared state across all processes
        jobs = manager.list()
        expected_output = manager.list()

        bot, jobs, expected_output = bot_processes(bot, jobs, expected_output)

        bot.start(processes=1)
        assert jobs[0] == 'init_complete'

        for cnt, job in enumerate(jobs[1:]):
            assert job.result_data == {'test': expected_output[cnt]}
            for func_not_run in ['preload', 'onload', 'preprocess',
                                 'process', 'precompletion',
                                 'postprocess']:
                # None of these functions should have been called because we
                # killed the process before they were called
                assert job.result_data != {'test': func_not_run}, \
                    "%s function ran when it shouldn't have" % func_not_run


@pytest.mark.xfail
def test_bot_receives_sets(mocker, qalx_session,
                           bot_config_class, user_config_class):
    """
    Tests that a bot runs through all the expected functions and processes
    them accordingly when it receives a set of items
    """
    # No response from status update
    status_update = {}
    get_queues = {
        'data': [queue_response],
    }

    get_item = entities_response['set'][0]
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')
    updated_replace_workers_post = copy.deepcopy(replace_workers_post)
    # We are only testing with a single worker
    updated_replace_workers_post['workers'].pop()
    workers_list_response = {'data': [workers[0]],
                             'query': {'next': None}}
    item_list_response = {
        'data': [entities_response['item'][0],
                 entities_response['item'][1],
                 entities_response['item'][2],
                 entities_response['item'][3]],
        'query': {'next': None}
    }
    mocked_api_request.side_effect = [
        # The first call creates a bot
        bot_post,
        updated_replace_workers_post,
        workers_list_response,
        status_update,
        get_queues,
        entities_response['set'][0],
        item_list_response
    ]
    mocked_boto3 = mocker.patch('pyqalx.core.entities.queue.boto3')
    mocked_boto3.client.return_value.receive_message.side_effect = [
        {'Messages': [{'Body': json.dumps({
            'entity_type': 'set',
            'entity_guid': get_item['guid']
        }),
            'ReceiptHandle': 'receipt handle'}]}
    ]

    bot = Bot(bot_name='test_bot',
              queue_name='test_queue',
              skip_ini=True,
              qalx_session_class=qalx_session.__class__,
              user_config_class=user_config_class,
              bot_config_class=bot_config_class)

    with Manager() as manager:
        # Use a manager for a shared state across all processes
        jobs = manager.list()
        expected_output = manager.list()

        bot, jobs, expected_output = bot_processes(bot, jobs, expected_output)

        bot.start(processes=1)
        assert jobs[0] == 'init_complete'

        for cnt, job in enumerate(jobs[1:]):
            assert job.result_data['test'] == expected_output[cnt]
            # This test case should never wait
            assert job.result_data != {'test': 'onwait'}, \
                "BotProcess called `onwait` function when it shouldn't have"
            if job.result_data['test'] == 'process':
                expected_items = {
                    'item1_guid':  entities_response['item'][0],
                    'item2_guid': entities_response['item'][1],
                    'item3_guid': entities_response['item'][2],
                    'item4_guid': entities_response['item'][3],
                }
                assert job.result_data['items'] == expected_items, \
                    'Items not added to job'
                assert 'sets' not in job.result_data.keys(), 'Unexpected sets'


@pytest.mark.xfail
def test_bot_receives_groups(mocker, qalx_session,
                             bot_config_class, user_config_class):
    """
    Tests that a bot runs through all the expected functions and processes
    them accordingly when it receives a group of sets
    """
    # No response from status update
    status_update = {}
    get_queues = {
        'data': [queue_response],
    }

    get_item = entities_response['group'][0]
    mocked_api_request = mocker.patch.object(QalxAdapter,
                                             '_process_api_request')
    updated_replace_workers_post = copy.deepcopy(replace_workers_post)
    # We are only testing with a single worker
    updated_replace_workers_post['workers'].pop()
    workers_list_response = {'data': [workers[0]],
                             'query': {'next': None}}
    set_list_response = {'data': [entities_response['set'][0],
                                  entities_response['set'][1], ],
                         'query': {'next': None}}
    item_list_response_1 = {'data': [entities_response['item'][0],
                                     entities_response['item'][1],
                                     entities_response['item'][2],
                                     entities_response['item'][3],],
                            'query': {'next': None}}
    item_list_response_2 = {'data': [entities_response['item'][0],
                                     entities_response['item'][1],
                                     entities_response['item'][3], ],
                            'query': {'next': None}}

    mocked_api_request.side_effect = [
        # The first call creates a bot
        bot_post,
        updated_replace_workers_post,
        workers_list_response,
        status_update,
        get_queues,
        entities_response['group'][0],
        set_list_response,
        item_list_response_1,
        item_list_response_2
    ]
    mocked_boto3 = mocker.patch('pyqalx.core.entities.queue.boto3')
    mocked_boto3.client.return_value.receive_message.side_effect = [
        {'Messages': [{'Body': json.dumps({
            'entity_type': 'group',
            'entity_guid': get_item['guid']
        }),
            'ReceiptHandle': 'receipt handle'}]}
    ]

    bot = Bot(bot_name='test_bot',
              queue_name='test_queue',
              skip_ini=True,
              user_config_class=user_config_class,
              qalx_session_class=qalx_session.__class__,
              bot_config_class=bot_config_class)

    with Manager() as manager:
        # Use a manager for a shared state across all processes
        jobs = manager.list()
        expected_output = manager.list()

        bot, jobs, expected_output = bot_processes(bot, jobs, expected_output)

        bot.start(processes=1)
        assert jobs[0] == 'init_complete'

        for cnt, job in enumerate(jobs[1:]):
            assert job.result_data['test'] == expected_output[cnt]
            # This test case should never wait
            assert job.result_data != {'test': 'onwait'}, \
                "BotProcess called `onwait` function when it shouldn't have"
            if job.result_data['test'] == 'process':
                set1 = entities_response['set'][0]
                set1['items'] = {'item1_guid': entities_response['item'][0],
                                 'item2_guid': entities_response['item'][1],
                                 'item3_guid': entities_response['item'][2],
                                 'item4_guid': entities_response['item'][3]}
                set2 = entities_response['set'][1]
                set2['items'] = {'item1_guid': entities_response['item'][0],
                                 'item2_guid': entities_response['item'][1],
                                 'item4_guid': entities_response['item'][3]}
                expected_sets = {
                    'set1_guid':  set1,
                    'set2_guid': set2,
                }
                assert 'items' not in job.result_data.keys(), 'Unexpected items'
                assert job.result_data['sets'] == expected_sets, \
                    'sets not added to job'


@pytest.mark.xfail
def test_bot_default_session_and_config(mocker):
    """
    Tests that if no session or config classes are supplied that the
    defaults are set correctly
    """
    mocker.patch.object(QalxAdapter, '_process_api_request')

    bot = Bot(queue_name='QUEUE NAME', bot_name='BOT NAME',
              skip_ini=True)
    assert isinstance(bot.bot_adapter.session,
                      QalxSession) is True
    assert isinstance(bot.bot_adapter.session.config,
                      BotConfig) is True
