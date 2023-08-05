import os

import pytest

from pyqalx.config import Config, BotConfig, UserConfig


def test_base_config_class():
    config = Config()
    assert not config.key_prefix
    assert not config.filename


@pytest.mark.parametrize("config_type,thing_returns,prefix", [
    (BotConfig, "A BOT THING", "QALX_BOT_"),
    (UserConfig, "A USER THING", "QALX_USER_")
])
def test_envvar_config(fake_environ, config_type, thing_returns, prefix):
    config = config_type()
    assert config['THING'] == thing_returns
    assert "SOME_OTHER_THING" not in config
    os.environ[prefix+"STUFF"] = thing_returns
    new_config = config_type()
    assert new_config["STUFF"] == thing_returns



@pytest.mark.parametrize("config_type", [BotConfig, UserConfig])
def test_botsinifile_config(mocker, config_type):
    mocked_path = mocker.patch('pyqalx.config.os.path.exists')
    mocked_path.return_value = True
    mo = mocker.mock_open(read_data="[default]\nSTUFF=SOME STUFF")
    mocker.patch('builtins.open', mo)

    config = config_type()
    config.from_inifile()
    mo.assert_called_once_with(config.config_path)
    assert config['STUFF'] == "SOME STUFF"
