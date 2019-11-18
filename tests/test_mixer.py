import mopidy.mixer
from mopidy_nad import mixer


def test_is_a_mopidy_mixer():
    assert issubclass(mixer.NadMixer, mopidy.mixer.Mixer)


# TODO Add more tests
