"""Mixer that controls volume using a NAD amplifier."""

from __future__ import unicode_literals

import logging

import pygst
pygst.require('0.10')
import gobject
import gst

try:
    import serial
except ImportError:
    serial = None  # noqa

from mopidy_nad import talker


logger = logging.getLogger(__name__)


class NadMixer(gst.Element, gst.ImplementsInterface, gst.interfaces.Mixer):
    __gstdetails__ = (
        'NadMixer',
        'Mixer',
        'Mixer to control NAD amplifiers using a serial link',
        'Mopidy')

    port = gobject.property(type=str, default='/dev/ttyUSB0')
    source = gobject.property(type=str)
    speakers_a = gobject.property(type=str)
    speakers_b = gobject.property(type=str)

    _volume_cache = 0
    _nad_talker = None

    def list_tracks(self):
        track = create_track(
            label='Master',
            initial_volume=0,
            min_volume=0,
            max_volume=100,
            num_channels=1,
            flags=(
                gst.interfaces.MIXER_TRACK_MASTER |
                gst.interfaces.MIXER_TRACK_OUTPUT))
        return [track]

    def get_volume(self, track):
        return [self._volume_cache]

    def set_volume(self, track, volumes):
        if len(volumes):
            volume = volumes[0]
            self._volume_cache = volume
            self._nad_talker.set_volume(volume)

    def set_mute(self, track, mute):
        self._nad_talker.mute(mute)

    def do_change_state(self, transition):
        if transition == gst.STATE_CHANGE_NULL_TO_READY:
            if serial is None:
                logger.warning('nadmixer dependency pyserial not found')
                return gst.STATE_CHANGE_FAILURE
            self._start_nad_talker()
        return gst.STATE_CHANGE_SUCCESS

    def _start_nad_talker(self):
        self._nad_talker = talker.NadTalker.start(
            port=self.port,
            source=self.source or None,
            speakers_a=self.speakers_a or None,
            speakers_b=self.speakers_b or None
        ).proxy()


def create_track(label, initial_volume, min_volume, max_volume,
                 num_channels, flags):

    class Track(gst.interfaces.MixerTrack):
        def __init__(self):
            super(Track, self).__init__()
            self.volumes = (initial_volume,) * self.num_channels

        @gobject.property
        def label(self):
            return label

        @gobject.property
        def min_volume(self):
            return min_volume

        @gobject.property
        def max_volume(self):
            return max_volume

        @gobject.property
        def num_channels(self):
            return num_channels

        @gobject.property
        def flags(self):
            return flags

    return Track()
