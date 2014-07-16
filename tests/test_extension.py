from __future__ import unicode_literals

import unittest

from mopidy_nad import Extension


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[nad]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('port = /dev/ttyUSB0', config)
        self.assertIn('source =', config)
        self.assertIn('speakers-a =', config)
        self.assertIn('speakers-b =', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('enabled', schema)
        self.assertIn('port', schema)
        self.assertIn('source', schema)
        self.assertIn('speakers-a', schema)
        self.assertIn('speakers-b', schema)
