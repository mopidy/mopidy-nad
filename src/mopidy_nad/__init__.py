import pathlib
from importlib.metadata import version
from typing import override

from mopidy import config, ext

__version__ = version("mopidy-nad")


class Extension(ext.Extension):
    dist_name = "mopidy-nad"
    ext_name = "nad"
    version = __version__

    @override
    def get_default_config(self) -> str:
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    @override
    def get_config_schema(self) -> config.ConfigSchema:
        schema = super().get_config_schema()
        schema["port"] = config.String()
        schema["source"] = config.String(optional=True)
        schema["speakers-a"] = config.Boolean(optional=True)
        schema["speakers-b"] = config.Boolean(optional=True)
        return schema

    @override
    def setup(self, registry: ext.Registry) -> None:
        from mopidy_nad.mixer import NadMixer  # noqa: PLC0415

        registry.add("mixer", NadMixer)
