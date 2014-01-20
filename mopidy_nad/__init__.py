from __future__ import unicode_literals

import os

import pygst
pygst.require('0.10')
import gst
import gobject

from mopidy import config, ext


__version__ = '1.1.0'


class Extension(ext.Extension):
    dist_name = 'Mopidy-NAD'
    ext_name = 'nad'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def setup(self, registry):
        from .mixer import NadMixer
        gobject.type_register(NadMixer)
        gst.element_register(NadMixer, 'nadmixer', gst.RANK_MARGINAL)
