from __future__ import unicode_literals

import unittest

import mopidy.mixer

from mopidy_nad import mixer


class MixerTest(unittest.TestCase):

    def test_is_a_mopidy_mixer(self):
        self.assert_(issubclass(mixer.NadMixer, mopidy.mixer.Mixer))

    # TODO Add more tests
