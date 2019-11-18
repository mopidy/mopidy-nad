from mopidy_nad import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert "[nad]" in config
    assert "enabled = true" in config
    assert "port = /dev/ttyUSB0" in config
    assert "source =" in config
    assert "speakers-a =" in config
    assert "speakers-b =" in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    assert "enabled" in schema
    assert "port" in schema
    assert "source" in schema
    assert "speakers-a" in schema
    assert "speakers-b" in schema
