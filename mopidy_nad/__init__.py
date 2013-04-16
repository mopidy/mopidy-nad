from __future__ import unicode_literals

import pygst
pygst.require('0.10')
import gst
import gobject

from mopidy import exceptions, ext


__version__ = '0.2'

default_config = b"""
[nad]
enabled = true
"""


class Extension(ext.Extension):
    dist_name = 'Mopidy-NAD'
    ext_name = 'nad'
    version = __version__

    def get_default_config(self):
        return default_config

    def validate_environment(self):
        try:
            import serial  # noqa
        except ImportError as e:
            raise exceptions.ExtensionError('pyserial library not found', e)

    def register_gstreamer_elements(self):
        from .mixer import NadMixer
        gobject.type_register(NadMixer)
        gst.element_register(NadMixer, 'nadmixer', gst.RANK_MARGINAL)
