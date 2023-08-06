# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import unittest

import upt

from upt_openbsd.upt_openbsd import OpenBSD


class TestOpenBSDBackend(unittest.TestCase):
    def setUp(self):
        self.openbsd_backend = OpenBSD()

    def test_unhandled_frontend(self):
        upt_pkg = upt.Package('foo', '42')
        upt_pkg.frontend = 'invalid frontend'
        with self.assertRaises(upt.UnhandledFrontendError):
            self.openbsd_backend.create_package(upt_pkg)


if __name__ == '__main__':
    unittest.main()
