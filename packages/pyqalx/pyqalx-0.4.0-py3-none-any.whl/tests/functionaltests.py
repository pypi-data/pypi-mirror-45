import itertools
import os
import threading
from collections import Counter
from os import environ
from random import randint, choice
from string import printable, whitespace
from tempfile import mkstemp, mkdtemp
from time import sleep
from uuid import uuid4

import pytest

from pyqalx import QalxSession, Bot
from pyqalx.core.errors import QalxAPIResponseError
from tests.conftest import FakeBotConfig as BaseFakeBotConfig, \
    FakeUserConfig as BaseFakeUserConfig


def append_short_uuid(prefix, uuid_lenth=6):
    return '_'.join([prefix, uuid4().hex[:uuid_lenth]])


DEV_CONFIGS = {"BASE_URL": environ.get("QALX_TEST_URL", "A FAKE TOKEN"),
               "TOKEN": environ.get("QALX_TEST_TOKEN", "A FAKE TOKEN")}


class FakeUserConfig(BaseFakeUserConfig):
    @property
    def defaults(self):
        config = super(FakeUserConfig, self).defaults
        config.update(DEV_CONFIGS)
        return config


class FakeBotConfig(BaseFakeBotConfig):
    @property
    def defaults(self):
        config = super(FakeBotConfig, self).defaults
        config.update({
            "MSG_BLACKOUTSECONDS": 30,
            "KILL_AFTER": 1,
            "WORKER_LOG_FILE_DIR": mkdtemp()

        })
        config.update(DEV_CONFIGS)
        return config


@pytest.fixture(scope="function")
def user_config_class():
    return FakeUserConfig


@pytest.fixture(scope="function")
def bot_config_class():
    return FakeBotConfig


_, tmp = mkstemp()


@pytest.fixture(scope="function")
def qalx_session(qalx_session_class, user_config_class):
    return qalx_session_class(config_class=user_config_class,
                              skip_ini=True)


@pytest.fixture(scope="function")
def test_bot_and_queue(qalx_session, user_config_class, bot_config_class):
    BOT_NAME = append_short_uuid("TEST_BOT_😁")
    QUEUE_NAME = append_short_uuid("TEST_QUEUE")

    bot = Bot(BOT_NAME, QUEUE_NAME, skip_ini=True,
              qalx_session_class=qalx_session.__class__,
              user_config_class=user_config_class,
              bot_config_class=bot_config_class)

    return bot, QUEUE_NAME


def test_add_item_data(qalx_session):
    item = qalx_session.item.add(data={"here_is": "some data"})
    assert item.get("guid")
    qalx_session.rest_api.delete(f"item/{item.get('guid')}")
    with pytest.raises(QalxAPIResponseError):
        qalx_session.item.get(guid=item.get('guid'))


def test_log_on_session(qalx_session):
    qalx_session.log.info("I LOGGED!")


def test_item_file(qalx_session):
    _handle, path = mkstemp()
    qalx_session.config['LOGGING_LEVEL'] = "info"
    qalx_session.log.info("path is " + path)
    os.close(_handle)
    random_string = ''.join([choice(printable + whitespace) for _ in range(1000)])
    with open(path, "w") as f:
        f.write(random_string)
    item = qalx_session.item.add_file(input_file=path)
    assert item.get("guid")
    archived_item = qalx_session.item.archive(entity=item)
    assert archived_item['info']['archived']
    item_guid = item['guid']
    item_by_guid = qalx_session.item.get(item_guid)


def f_init(qalx_session):
    print('initialisation')
    return True


def f_begin(job):
    print('begin')


def f_preload(job):
    print('preload')
    job.add_step_result(True, {"test": "functional"})


def f_onload(job):
    print('onload')
    job.entity['data']['onload'] = True
    job.add_step_result(True, {"test": "functional"})


def f_preprocess(job):
    print('preprocess')
    job.entity['data']['preprocess'] = True
    job.add_step_result(True, {"test": "functional"})


def f_process(job):
    how_long = job.entity['data']['how long?']
    sleep(how_long)
    guid = job.entity['guid']
    print(f'process takes {how_long}s on {guid[-6:]}')
    job.entity['data']['process'] = True
    job.add_step_result(True, {"test": "functional"})


def f_precompletion(job):
    print('precompletion')
    job.entity['data']['precompletion'] = True
    job.add_step_result(True, {"test": "functional"})


def f_postprocess(job):
    print('postprocess')
    job.entity['data']['postprocess'] = True
    job.add_step_result(True, {"test": "functional"})


def f_onwait(job):
    print('onwait')
    job.add_step_result(True, {"test": "functional"})


def f_ontermination(job):
    print('ontermination')
    job.add_step_result(True, {"test": "functional"})


def test_bot_items(qalx_session, test_bot_and_queue):
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.add(queue_name)

    items = []
    for n in range(10):
        item = qalx_session.item.add(data={"some_data_to_process": "some data",
                                           "how long?": randint(2, 10)})
        queue.submit_entity(item)
        items.append(item)

    test_bot.initialisation_function = f_init
    test_bot.begin_function = f_begin
    test_bot.preload_function = f_preload
    test_bot.onload_function = f_onload
    test_bot.preprocess_function = f_preprocess
    test_bot.process_function = f_process
    test_bot.precompletion_function = f_precompletion
    test_bot.postprocess_function = f_postprocess
    test_bot.onwait_function = f_onwait
    test_bot.ontermination_function = f_ontermination
    test_bot.start(4)
    life_cycle = ('onload',
                  'preprocess',
                  'process',
                  'precompletion',
                  'postprocess')

    for ui in items:
        updated_item = qalx_session.item.get(ui['guid'])
        for part in life_cycle:
            assert updated_item['data'].get(part)
    session = QalxSession(config_class=test_bot.bot_adapter.session.config.__class__)
    remaining_messages = session.queue.get_messages(queue)
    assert len(remaining_messages) == 0, 'Messages not deleted from queue'


def beam_calcs(job):
    shape_data = job.entity.get_item_data("shape")  # get the shape item data from the set
    density_data = job.entity.get_item_data("density")  # get the density item data from the set
    load_data = job.entity.get_item_data("load")  # get the load item data from the set
    length_data = job.entity.get_item_data("length")  # get the length item data from the set

    # define a stress calculation function
    def stress_of_beam_in_bending(length, breadth, thickness, density, udl):
        """ calculates bending stress in a simply supported beam
        """
        load = 9.81 * (udl + density * breadth * thickness)
        max_moment = (load * length ** 2) / 8
        I = (breadth * thickness ** 3) / 12
        y = thickness / 2
        return max_moment / (I / y)

    max_stress = stress_of_beam_in_bending(
        length_data['value'],
        shape_data['breadth'],
        shape_data['thickness'],
        density_data['value'],
        load_data['value'],
    )

    print(job.entity['meta']['set_name'], max_stress)
    job.add_item_data("stress", data={
        "result": "stress_of_beam_in_bending",
        "value": max_stress,
        "units": "MPa"
    })


def test_example_set(qalx_session, test_bot_and_queue):
    qalx_session.config['LOGGING_LEVEL'] = "info"
    test_bot, queue_name = test_bot_and_queue
    specs = [
        {"CODE": "10 X 3MM", "thickness": 3e-3, "breadth": 10e-3},
        {"CODE": "13 X 3MM", "thickness": 3e-3, "breadth": 13e-3},
    ]

    uniform_loads = range(2, 11, 4)
    lengths = range(4, 7, 1)
    density = qalx_session.item.add(data={"value": 7850, "units": "kg/m^3"},
                                    meta={"material": "steel", "property": "density"})

    sets = {}
    for s, l, udl in itertools.product(specs, lengths, uniform_loads):
        shape = qalx_session.item.add(data=s, meta={"shape_source": "beam-spec-123"})
        length = qalx_session.item.add(data={"value": l, "units": "m"})
        load = qalx_session.item.add(data={"value": udl, "units": "kg/m"})
        set_name = f"{s['CODE']} @ {l} under {udl}"

        sets[set_name] = qalx_session.set.add(items={
            "shape": shape,
            "density": density,
            "load": load,
            "length": length
        }, meta={"set_name": set_name})

    group = qalx_session.group.add(sets=sets, meta={"batch": "Flat bar of mild steel"})

    queue = qalx_session.queue.get_or_create(name=queue_name)
    queue.submit_sets_from_group(group)

    test_bot.process_function = beam_calcs
    test_bot.start(1)

    for key, s in sets.items():
        stressed_set = qalx_session.set.get(s['guid'])
        assert "stress" in stressed_set['items']  # will only work if the bot added the stress item

    # test searching and sorting
    stress_items = qalx_session.item.list(data="result=stress_of_beam_in_bending", sort="-value")
    worst_stress = stress_items['data'][0]
    assert worst_stress


def test_with_decorators(qalx_session, test_bot_and_queue):
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    for n in range(2):
        i = qalx_session.item.add(data={"n": n})
        queue.submit_entity(i)

    @test_bot.process
    def do_process(job):
        job.log.error(job.entity['data']['n'])
        print(job.entity['data']['n'])

    test_bot.start(1)


@pytest.mark.slow
def test_send_signal_to_bot_warm(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker.  We warm terminate the
    bot which should cause the bot to stop processing after all processing of
    the first item is completed.
    The second item won't get processed.
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.entity['data']['complete'] = True
        sleep(20)
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1
    qalx_session.bot.terminate(test_bot.bot_entity)  # kill the bot
    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert not item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_worker_warm(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker.  We warm terminate the
    worker which should kill the worker (and thus the bot) after
    all processing of the first item is completed.
    The second item won't get processed.
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.entity['data']['complete'] = True
        sleep(20)
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1
    bot = qalx_session.bot.reload(test_bot.bot_entity)
    bot_entity, worker_guid = bot, bot['workers'][0]['guid']
    worker = qalx_session.worker.get(bot_entity=bot_entity, guid=worker_guid)
    # kill the worker
    qalx_session.worker.terminate(worker, bot_entity=bot_entity, warm=True)
    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert not item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_worker_cold(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker.  We cold terminate the
    worker which should kill the worker (and thus the bot) as soon as possible
    during processing
    Neither item will get processed.
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.preprocess
    def preprocess_terminate(job):
        """
        We terminate the worker in the preprocess stage.  This will prevent
        the `@test_bot.process` function from being run
        """
        job.worker_adapter.terminate(job._worker_entity,
                                     bot_entity=job._bot_entity,
                                     warm=False)

    @test_bot.process
    def do_thing(job):
        sleep(20)
        job.entity['data']['complete'] = True
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1

    while bot_thread.is_alive():  # wait for it to die
        sleep(5)

    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)
    assert not item_1['data'].get('complete')
    assert not item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_job_warm(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker.  We warm terminate the
    worker via the job which should kill the worker (and thus the bot) after
    all processing of the first item is completed.
    The second item won't get processed.
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.terminate()
        sleep(20)
        job.save_entity()

    @test_bot.postprocess
    def mark_complete(job):
        job.entity['data']['complete'] = True
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1

    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert not item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_job_cold(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker.  We cold terminate the
    worker via the job which should kill the worker (and thus the bot) as soon
    as possible during processing
    Neither item will get processed.
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.terminate(warm=False)
        sleep(20)
        job.save_entity()

    @test_bot.postprocess
    def mark_complete(job):
        job.entity['data']['complete'] = True
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1

    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert not item_1['data'].get('complete')
    assert not item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_worker_stop(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker. Stopping processing of the
    worker for a period of time and then restarting the worker.
    Both items should be processed but won't be processed while the worker
    is stopped
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.entity['data']['complete'] = True
        sleep(20)
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1
    bot = qalx_session.bot.reload(test_bot.bot_entity)
    bot_entity, worker_guid = bot, bot['workers'][0]['guid']
    worker = qalx_session.worker.get(bot_entity=bot_entity, guid=worker_guid)
    qalx_session.worker.stop(worker, bot_entity=bot)  # kill the bot
    n_waited = 0
    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
        if n_waited >= 5:
            qalx_session.worker.resume(worker, bot_entity=bot)
        else:
            item_2 = qalx_session.item.reload(item_2)
            print(item_2['data'].get('complete'), item_2)
            assert not item_2['data'].get('complete')
            n_waited += 1

    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_bot_stop(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker. Stopping processing of the
    bot for a period of time and then restarting the bot.
    Both items should be processed but won't be processed while the bot is
    stopped
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        sleep(20)
        job.entity['data']['complete'] = True
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(10)  # let the bot get started on job 1
    bot = qalx_session.bot.reload(test_bot.bot_entity)
    qalx_session.bot.stop(bot)  # kill the bot
    n_waited = 0
    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
        if n_waited >= 5:
            qalx_session.bot.resume(bot)
        else:

            assert not item_2['data'].get('complete')
            n_waited += 1

    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert item_2['data'].get('complete')


@pytest.mark.slow
def test_send_signal_to_stop_one_worker(qalx_session, test_bot_and_queue):
    """
    Tests submitting ten items with a two workers. Stopping processing of
    one of the workers after the first job has started processing and then
    resuming it after all other jobs have completed.
    The first two jobs will be run on both workers but all subsequent jobs
    will be run on only a single worker
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    items = []
    for i in range(10):
        item = qalx_session.item.add(data={"job": i})
        queue.submit_entity(item)
        items.append(item)

    @test_bot.process
    def do_thing(job):
        sleep(10)
        job.entity['data']['complete'] = True
        job.entity['data']['run_on'] = job._worker_entity['guid']
        job.save_entity()
        print(dict(job.entity))

    bot_thread = threading.Thread(target=test_bot.start, args=(2,))
    bot_thread.start()
    sleep(5)  # let the bot get started on job 1
    bot = qalx_session.bot.reload(test_bot.bot_entity)
    bot_entity, worker_guid = bot, bot['workers'][0]['guid']

    worker = qalx_session.worker.get(bot_entity=bot_entity, guid=worker_guid)
    qalx_session.worker.stop(worker, bot_entity=bot)  # kill the bot
    last_complete = False
    while bot_thread.is_alive():  # wait for it to die
        sleep(5)
        item = qalx_session.item.reload(items[-1])
        if last_complete:
            qalx_session.worker.resume(worker, bot_entity=bot)
        else:
            print(item['data'].get('complete'), item['data'].get('run_on'), item)
            if item['data'].get('complete'):
                last_complete = True

    counter = Counter([qalx_session.item.reload(i)['data']['run_on'] for i in items])
    assert counter[worker_guid] == 1


@pytest.mark.slow
def test_send_signal_to_job_stop_processing(qalx_session, test_bot_and_queue):
    """
    Tests submitting two items with a single worker. Stopping processing of
    one of the workers via the job and then restarting the worker via the job
    after a period of time.
    Both items will be processed but the first item will have more waits
    """
    test_bot, queue_name = test_bot_and_queue
    queue = qalx_session.queue.get_or_create(queue_name)
    item_1 = qalx_session.item.add(data={"job": 1, "waits": 0})
    queue.submit_entity(item_1)
    item_2 = qalx_session.item.add(data={"job": 2, "waits": 0})
    queue.submit_entity(item_2)

    @test_bot.process
    def do_thing(job):
        job.entity['data']['complete'] = True
        job.save_entity()
        if job.entity['data']['job'] == 1:
            # Only stop processing on the first job.  The second job should
            # just go through normally
            job.stop_processing()
        sleep(5)

    @test_bot.onwait
    def do_wait(job):
        job.entity['data']['waits'] += 1

        if job.entity['data'].get('waits') == 5:
            job.resume_processing()
        job.save_entity()

    bot_thread = threading.Thread(target=test_bot.start)
    bot_thread.start()
    sleep(1)  # let the bot get started on job 1

    bot = qalx_session.bot.reload(test_bot.bot_entity)
    bot_entity, worker_guid = bot, bot['workers'][0]['guid']
    worker = qalx_session.worker.get(bot_entity=bot_entity, guid=worker_guid)
    qalx_session.worker.stop(worker, bot_entity=bot)  # kill the worker
    while bot_thread.is_alive():  # wait for it to die
        sleep(2)
        print(qalx_session.item.reload(item_1)['data'])
        print(qalx_session.item.reload(item_2)['data'])

    item_1 = qalx_session.item.reload(item_1)
    item_2 = qalx_session.item.reload(item_2)

    assert item_1['data'].get('complete')
    assert item_1['data'].get('waits') == 5
    assert item_2['data'].get('complete')
    # This will be 1 because we will have waited once to see if there are any
    # further messages
    assert item_2['data'].get('waits') == 1
