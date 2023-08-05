import functools
import os
from tempfile import mkstemp

import pytest

from pyqalx import QalxSession
from pyqalx.config import UserConfig, BotConfig


log_handle, temp_log_path = mkstemp()
os.close(log_handle)


class FakeQalx(QalxSession):
    pass


class FakeUserConfig(UserConfig):
    @property
    def defaults(self):
        config = super(FakeUserConfig, self).defaults
        to_update = dict(
            TOKEN="",  # no token is available by default
            MSG_WAITTIMESECONDS=20,
            # calls to the remote queue will not return for this long
            MSG_BLACKOUTSECONDS=30,
            # messages must be removed from the queue within this time after reading
            LOG_FILE_PATH=temp_log_path,
            LOGGING_LEVEL="INFO",
            UNPACK_SET=True,
            UNPACK_GROUP=True,
            UNPACK_BOT=True
        )
        config.update(to_update)
        return config


class FakeBotConfig(BotConfig):
    @property
    def defaults(self):
        config = super(FakeBotConfig, self).defaults
        config.update(FakeUserConfig().defaults)
        return config


@pytest.fixture
def qalx_session_class():
    """
    Helper function for getting our qalx test class in case we want to
    override anything in the future
    :return: FakeQalx class
    """
    return FakeQalx


@pytest.fixture
def user_config_class():
    """
    Helpers for getting our test UserConfig
    :return:
    """
    return FakeUserConfig


@pytest.fixture
def bot_config_class(user_config_class):
    """
    Fixture for the test BotConfig.  Uses the defaults on the BotConfig
    and then overrides the test values with that on the UserConfig as we want
    to use all the same defaults for testing
    :return:
    """
    return FakeBotConfig


@pytest.fixture()
def qalx_session(qalx_session_class, user_config_class):
    return qalx_session_class(config_class=user_config_class,
                              skip_ini=True)


@pytest.fixture
def fake_environ(mocker):
    mocker.patch.dict('pyqalx.config.os.environ',
                      QALX_BOT_THING="A BOT THING",
                      QALX_USER_THING="A USER THING",
                      SOME_OTHER_THING="SECRET")
    return mocker
