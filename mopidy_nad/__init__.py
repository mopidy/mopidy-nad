import os

import pkg_resources

from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-NAD").version


class Extension(ext.Extension):
    dist_name = "Mopidy-NAD"
    ext_name = "nad"
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), "ext.conf")
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["port"] = config.String()
        schema["source"] = config.String(optional=True)
        schema["speakers-a"] = config.Boolean(optional=True)
        schema["speakers-b"] = config.Boolean(optional=True)
        return schema

    def setup(self, registry):
        from mopidy_nad.mixer import NadMixer

        registry.add("mixer", NadMixer)
