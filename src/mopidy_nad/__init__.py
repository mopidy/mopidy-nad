import pathlib
from importlib.metadata import version

from mopidy import config, ext

__version__ = version("mopidy-nad")


class Extension(ext.Extension):
    dist_name = "mopidy-nad"
    ext_name = "nad"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["port"] = config.String()
        schema["source"] = config.String(optional=True)
        schema["speakers-a"] = config.Boolean(optional=True)
        schema["speakers-b"] = config.Boolean(optional=True)
        return schema

    def setup(self, registry):
        from mopidy_nad.mixer import NadMixer  # noqa: PLC0415

        registry.add("mixer", NadMixer)
