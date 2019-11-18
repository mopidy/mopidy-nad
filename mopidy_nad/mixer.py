"""Mixer that controls volume using a NAD amplifier."""

import logging

import pykka

import serial
from mopidy import mixer

logger = logging.getLogger(__name__)


class NadMixer(pykka.ThreadingActor, mixer.Mixer):

    name = "nad"

    def __init__(self, config):
        super().__init__(config)

        self.port = config["nad"]["port"]
        self.source = config["nad"]["source"] or None
        self.speakers_a = config["nad"]["speakers-a"]
        self.speakers_b = config["nad"]["speakers-b"]

        self._volume_cache = 0
        self._mute_cache = False

        self._device = None

        # Volume in range 0..VOLUME_LEVELS, None before calibration.
        self._nad_volume = None

    def get_volume(self):
        return self._volume_cache

    def set_volume(self, volume):
        success = self._set_volume(volume)
        if success:
            self._volume_cache = volume
            self.trigger_volume_changed(volume)
        return success

    def get_mute(self):
        return self._mute_cache

    def set_mute(self, mute):
        success = self._mute(mute)
        if success:
            self._mute_cache = mute
            self.trigger_mute_changed(mute)
        return success

    # Serial link config
    BAUDRATE = 115200
    BYTESIZE = 8
    PARITY = "N"
    STOPBITS = 1

    # Timeout in seconds used for read/write operations.
    # If you set the timeout too low, the reads will never get complete
    # confirmations and calibration will decrease volume forever. If you set
    # the timeout too high, stuff takes more time. 0.2s seems like a good value
    # for NAD C 355BEE.
    TIMEOUT = 0.2

    # Number of volume levels the amplifier supports. 40 for NAD C 355BEE.
    VOLUME_LEVELS = 40

    def on_start(self):
        self._open_connection()
        self._set_device_to_known_state()

    def _open_connection(self):
        logger.info(f"NAD mixer: Connecting through {self.port!r}")
        self._device = serial.Serial(
            port=self.port,
            baudrate=self.BAUDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT,
        )
        self._get_device_model()

    def _set_device_to_known_state(self):
        self._power_device_on()
        self._select_speakers()
        self._select_input_source()
        self._mute(False)
        self.calibrate_volume()

    def _get_device_model(self):
        model = self._ask_device("Main.Model")
        logger.info(f"NAD mixer: Connected to model {model!r}")
        return model

    def _power_device_on(self):
        self._check_and_set("Main.Power", "On")

    def _select_speakers(self):
        if self.speakers_a is not None:
            self._check_and_set(
                "Main.SpeakerA", "On" if self.speakers_a else "Off"
            )
        if self.speakers_b is not None:
            self._check_and_set(
                "Main.SpeakerB", "On" if self.speakers_b else "Off"
            )

    def _select_input_source(self):
        if self.source is not None:
            self._check_and_set("Main.Source", self.source.title())

    def _mute(self, mute):
        if mute:
            return self._check_and_set("Main.Mute", "On")
        else:
            return self._check_and_set("Main.Mute", "Off")

    def calibrate_volume(self, current_nad_volume=None):
        # The NAD C 355BEE amplifier has 40 different volume levels. We have no
        # way of asking on which level we are. Thus, we must calibrate the
        # mixer by decreasing the volume 39 times.
        if current_nad_volume is None:
            current_nad_volume = self.VOLUME_LEVELS
        if current_nad_volume == self.VOLUME_LEVELS:
            logger.info("NAD mixer: Calibrating by setting volume to 0")
        self._nad_volume = current_nad_volume
        if self._decrease_volume():
            current_nad_volume -= 1
        if current_nad_volume == 0:
            logger.info("NAD mixer: Done calibrating")
        else:
            self.actor_ref.proxy().calibrate_volume(current_nad_volume)

    def _set_volume(self, volume):
        # Increase or decrease the amplifier volume until it matches the given
        # target volume.
        logger.debug(f"Setting volume to {volume}")
        target_nad_volume = int(round(volume * self.VOLUME_LEVELS / 100.0))
        if self._nad_volume is None:
            return False  # Calibration needed
        while target_nad_volume > self._nad_volume:
            if self._increase_volume():
                self._nad_volume += 1
        while target_nad_volume < self._nad_volume:
            if self._decrease_volume():
                self._nad_volume -= 1
        return True

    def _increase_volume(self):
        # Increase volume. Returns :class:`True` if confirmed by device.
        self._write("Main.Volume+")
        return self._readline() == "Main.Volume+"

    def _decrease_volume(self):
        # Decrease volume. Returns :class:`True` if confirmed by device.
        self._write("Main.Volume-")
        return self._readline() == "Main.Volume-"

    def _check_and_set(self, key, value):
        for attempt in range(1, 4):
            if self._ask_device(key) == value:
                return True
            logger.info(
                f"NAD mixer: Setting {key!r} to {value!r} (attempt {attempt}/3)"
            )
            self._command_device(key, value)
        if self._ask_device(key) == value:
            return True
        else:
            logger.warning(
                f"NAD mixer: Gave up on setting {key!r} to {value!r}"
            )
            return False

    def _ask_device(self, key):
        self._write("%s?" % key)
        return self._readline().replace(f"{key}=", "")

    def _command_device(self, key, value):

        self._write(f"{key}={value}")
        self._readline()

    def _write(self, data: str):
        # Write data to device. Prepends and appends a newline to the data, as
        # recommended by the NAD documentation.
        if not self._device.isOpen():
            self._device.open()
        data_bytes = f"\n{data}\n".encode()
        self._device.write(data_bytes)
        logger.debug(f"Write: {data_bytes!r}")

    def _readline(self) -> str:
        # Read line from device. The result is stripped for leading and
        # trailing whitespace.
        if not self._device.isOpen():
            self._device.open()
        result_bytes = self._device.readline().strip()
        if result_bytes:
            logger.debug(f"Read: {result_bytes!r}")
        result = result_bytes.decode()
        return result
