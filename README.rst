**********
Mopidy-NAD
**********

`Mopidy <http://www.mopidy.com/>`_ extension for controlling volume using an
external NAD amplifier. Developed and tested with a NAD C355BEE.

Installation
============

Install by running::

    sudo pip install Mopidy-NAD

Or install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

The Mopidy-NAD extension is enabled by default. To disable it, add the
following to ``mopidy.conf``::

    [nad]
    enabled = false

The NAD amplifier must be connected to the machine running Mopidy using a
serial cable.

To use the NAD amplifier ot control volume, set the ``audio/mixer`` config
value in ``mopidy.conf`` to ``nadmixer``. You probably also needs to add some
properties to the ``audio/mixer`` config value.

Supported properties includes:

``port``:
    The serial device to use, defaults to ``/dev/ttyUSB0``. This must be
    set correctly for the mixer to work.

``source``:
    The source that should be selected on the amplifier, like ``aux``,
    ``disc``, ``tape``, ``tuner``, etc. Leave unset if you don't want the
    mixer to change it for you.

``speakers-a``:
    Set to ``on`` or ``off`` if you want the mixer to make sure that
    speaker set A is turned on or off. Leave unset if you don't want the
    mixer to change it for you.

``speakers-b``:
    See ``speakers-a``.

Configuration examples::

    # Minimum configuration, if the amplifier is available at /dev/ttyUSB0
    [audio]
    mixer = nadmixer

    # Minimum configuration, if the amplifier is available elsewhere
    [audio]
    mixer = nadmixer port=/dev/ttyUSB3

    # Full configuration
    [audio]
    mixer = nadmixer port=/dev/ttyUSB0 source=aux speakers-a=on speakers-b=off


Project resources
=================

- `Source code <https://github.com/mopidy/mopidy-nad>`_
- `Issue tracker <https://github.com/mopidy/mopidy/issues>`_
- `Download development snapshot <https://github.com/mopidy/mopidy-nad/tarball/develop#egg=Mopidy-NAD-dev>`_


Changelog
=========

v0.3 (2013-04-16)
-----------------

- Include ``README.rst`` and ``LICENSE`` in PyPI package.

v0.2 (2013-04-16)
-----------------

- Add missing ``create_track()`` helper function.

v0.1 (2013-04-16)
-----------------

- Extracted extension from Mopidy core.
