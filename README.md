# mopidy-nad

[![Latest PyPI version](https://img.shields.io/pypi/v/mopidy-nad)](https://pypi.org/p/mopidy-nad)
[![CI build status](https://img.shields.io/github/actions/workflow/status/mopidy/mopidy-nad/ci.yml)](https://github.com/mopidy/mopidy-nad/actions/workflows/ci.yml)
[![Test coverage](https://img.shields.io/codecov/c/gh/mopidy/mopidy-nad)](https://codecov.io/gh/mopidy/mopidy-nad)

[Mopidy](https://mopidy.com) extension for controlling volume on a NAD amplifier.
Developed and tested with a NAD C355BEE.


## Maintainer wanted

Mopidy-NAD is currently kept on life support by the Mopidy core developers.
It is in need of a more dedicated maintainer.

If you want to be the maintainer of Mopidy-NAD, please:

1. Make 2-3 good pull requests improving any part of the project.

2. Read and get familiar with all of the project's open issues.

3. Send a pull request removing this section and adding yourself as the
   "Current maintainer" in the "Credits" section below. In the pull request
   description, please refer to the previous pull requests and state that
   you've familiarized yourself with the open issues.

As a maintainer, you'll be given push access to the repo and the authority to
make releases to PyPI when you see fit.


## Installation

Install by running:

```sh
python3 -m pip install mopidy-nad
```

See https://mopidy.com/ext/nad/ for alternative installation methods.


## Configuration

The Mopidy-NAD extension is enabled by default. To disable it, add the
following to `mopidy.conf`:

```ini
[nad]
enabled = false
```

The NAD amplifier must be connected to the machine running Mopidy using a
serial cable.

To use the NAD amplifier to control volume, set the `audio/mixer` config
value in `mopidy.conf` to `nad`. You probably also needs to add some
properties to the `nad` config section.

Supported properties includes:

- `port`: The serial device to use, defaults to `/dev/ttyUSB0`. This must
  be set correctly for the mixer to work.

- `source`: The source that should be selected on the amplifier, like
  `aux`, `disc`, `tape`, `tuner`, etc. Leave unset if you don't want
  the mixer to change it for you.

- `speakers-a`: Set to `on` or `off` (or `true` or `false`) if you
  want the mixer to make sure that speaker set A is turned on or off. Leave
  unset if you don't want the mixer to change it for you.

- `speakers-b`: See `speakers-a`.

Configuration example with minimum configuration, if the amplifier is available
at `/dev/ttyUSB0`::

```ini
[audio]
mixer = nad
```

Configuration example with minimum configuration, if the amplifier is available
elsewhere:

```ini
[audio]
mixer = nad

[nad]
port = /dev/ttyUSB3
```

Configuration example with full configuration::

```ini
[audio]
mixer = nad

[nad]
port = /dev/ttyUSB0
source = aux
speakers-a = true
speakers-b = false
```


## Project resources

- [Source code](https://github.com/mopidy/mopidy-nad)
- [Issues](https://github.com/mopidy/mopidy-nad/issues)
- [Releases](https://github.com/mopidy/mopidy-nad/releases)


## Development

### Set up development environment

Clone the repo using, e.g. using [gh](https://cli.github.com/):

```sh
gh repo clone mopidy/mopidy-nad
```

Enter the directory, and install dependencies using [uv](https://docs.astral.sh/uv/):

```sh
cd mopidy-nad/
uv sync
```

### Running tests

To run all tests and linters in isolated environments, use
[tox](https://tox.wiki/):

```sh
tox
```

To only run tests, use [pytest](https://pytest.org/):

```sh
pytest
```

To format the code, use [ruff](https://docs.astral.sh/ruff/):

```sh
ruff format .
```

To check for lints with ruff, run:

```sh
ruff check .
```

To check for type errors, use [pyright](https://microsoft.github.io/pyright/):

```sh
pyright .
```

### Making a release

To make a release to PyPI, go to the project's [GitHub releases
page](https://github.com/mopidy/mopidy-nad/releases)
and click the "Draft a new release" button.

In the "choose a tag" dropdown, select the tag you want to release or create a
new tag, e.g. `v0.1.0`. Add a title, e.g. `v0.1.0`, and a description of the changes.

Decide if the release is a pre-release (alpha, beta, or release candidate) or
should be marked as the latest release, and click "Publish release".

Once the release is created, the `release.yml` GitHub Action will automatically
build and publish the release to
[PyPI](https://pypi.org/project/mopidy-nad/).


## Credits

- Original author: [Stein Magnus Jodal](https://github.com/jodal)
- Current maintainer: None. Maintainer wanted, see section above.
- [Contributors](https://github.com/mopidy/mopidy-nad/graphs/contributors)
