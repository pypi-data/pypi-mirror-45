# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import os
import unittest
from unittest import mock

import upt

from upt_openbsd.upt_openbsd import OpenBSDPackage


class TestOpenBSDPackage(unittest.TestCase):
    def setUp(self):
        self.obsd_pkg = OpenBSDPackage()
        self.obsd_pkg.upt_pkg = upt.Package('foo', '42')

    def test_summary(self):
        self.obsd_pkg.upt_pkg.summary = 'perfectly OK'
        expected = 'perfectly OK'
        self.assertEqual(self.obsd_pkg._summary(), expected)

        self.obsd_pkg.upt_pkg.summary = 'Uppercase'
        expected = 'uppercase'
        self.assertEqual(self.obsd_pkg._summary(), expected)

        self.obsd_pkg.upt_pkg.summary = 'A framework'
        self.assertEqual(self.obsd_pkg._summary(), 'framework')

        self.obsd_pkg.upt_pkg.summary = 'a framework'
        self.assertEqual(self.obsd_pkg._summary(), 'framework')

        self.obsd_pkg.upt_pkg.summary = 'An animal'
        self.assertEqual(self.obsd_pkg._summary(), 'animal')

        self.obsd_pkg.upt_pkg.summary = 'an animal'
        self.assertEqual(self.obsd_pkg._summary(), 'animal')

        self.obsd_pkg.upt_pkg.summary = 'No period.'
        self.assertEqual(self.obsd_pkg._summary(), 'no period')

        self.obsd_pkg.upt_pkg.summary = 'this is ok, etc.'
        self.assertEqual(self.obsd_pkg._summary(), 'this is ok, etc.')

    def test_non_implemented_functions(self):
        # These functions must be implemented by the subclasses of
        # OpenBSDPackage, since there is no "generic" implementation. We need
        # to make sure they stay unimplemented in OpenBSDPackage.
        self.assertRaises(NotImplementedError, self.obsd_pkg._pkgname)
        self.assertRaises(NotImplementedError, self.obsd_pkg._distname)
        self.assertRaises(NotImplementedError,
                          self.obsd_pkg._normalized_openbsd_name,
                          'foo')


class TestDirectoryCreation(unittest.TestCase):
    def setUp(self):
        self.obsd_pkg = OpenBSDPackage()
        self.obsd_pkg.upt_pkg = upt.Package('foo', '42')
        self.obsd_pkg.upt_pkg.frontend = 'frontend'
        self.obsd_pkg._normalized_openbsd_name = lambda x: x

    @mock.patch('os.makedirs')
    def test_create_directories_no_output(self, m_mkdir):
        self.obsd_pkg._create_output_directories(self.obsd_pkg.upt_pkg, None)
        m_mkdir.assert_called_with('/usr/ports/mystuff/frontend/foo/pkg')

    @mock.patch.dict(os.environ, {'PORTSDIR': '/path/to/ports'}, clear=True)
    @mock.patch('os.makedirs')
    def test_create_directories_no_output_environ(self, m_mkdir):
        self.obsd_pkg._create_output_directories(self.obsd_pkg.upt_pkg, None)
        m_mkdir.assert_called_with('/path/to/ports/mystuff/frontend/foo/pkg')

    @mock.patch('os.makedirs')
    def test_create_directories_output(self, m_mkdir):
        self.obsd_pkg._create_output_directories(self.obsd_pkg.upt_pkg,
                                                 '/ports/')
        m_mkdir.assert_called_with('/ports/pkg')

    @mock.patch('os.makedirs', side_effect=PermissionError)
    def test_create_directories_permission_error(self, m_makedirs):
        with self.assertRaises(SystemExit):
            self.obsd_pkg._create_output_directories(self.obsd_pkg.upt_pkg,
                                                     '/ports/')

    @mock.patch('os.makedirs', side_effect=FileExistsError)
    def test_create_directories_file_exists(self, m_makedirs):
        with self.assertRaises(SystemExit):
            self.obsd_pkg._create_output_directories(self.obsd_pkg.upt_pkg,
                                                     '/ports/')


class TestFileCreation(unittest.TestCase):
    def setUp(self):
        self.obsd_pkg = OpenBSDPackage()
        self.obsd_pkg.output_dir = '/outdir'
        archives = [
            upt.Archive('http://www.example.com/src.tar.gz', size=1337,
                        sha256_base64='sha256_base64')
        ]
        self.obsd_pkg.upt_pkg = upt.Package('foo', '42',
                                            description='descr',
                                            archives=archives)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch.object(OpenBSDPackage, '_render_makefile_template',
                       return_value='Makefile content')
    def test_makefile_creation(self, m_makefile, m_open):
        self.obsd_pkg._create_makefile()
        m_open.assert_called_once_with('/outdir/Makefile', 'w',
                                       encoding='utf-8')
        m_open().write.assert_called_once_with('Makefile content')

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_distinfo_creation(self, m_open):
        self.obsd_pkg._create_distinfo()
        m_open.assert_called_once_with('/outdir/distinfo', 'w',
                                       encoding='utf-8')
        # XXX Testing calls to "write" is not really good here, but that is the
        # simplest way of getting something to work.
        text = 'SHA256 (src.tar.gz) = sha256_base64\n'
        m_open().write.assert_any_call(text)
        text = 'SIZE (src.tar.gz) = 1337\n'
        m_open().write.assert_any_call(text)

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_pkgdescr_creation(self, m_open):
        self.obsd_pkg._create_pkg_descr()
        m_open.assert_called_once_with('/outdir/pkg/DESCR', 'w',
                                       encoding='utf-8')
        m_open().write.assert_called_once_with('descr')


class TestOpenBSDPackageWithoutSQLPorts(unittest.TestCase):
    def setUp(self):
        OpenBSDPackage.SQLPORTS_DB = '/does/not/exist'

    def test_sqlports_init(self):
        with OpenBSDPackage() as package:
            self.assertIsNone(package.conn)

    def test_sqlports_fullpkgpath(self):
        with OpenBSDPackage() as package:
            out = package._to_openbsd_fullpkgpath('py-requests')
            expected = 'xxx/py-requests'
            self.assertEqual(out, expected)


class TestOpenBSDPackageWithSQLPorts(unittest.TestCase):
    def setUp(self):
        OpenBSDPackage.SQLPORTS_DB = ':memory:'
        self.package = OpenBSDPackage()
        self.package.conn.execute('''CREATE TABLE IF NOT EXISTS `Ports` (
    `FULLPKGPATH` TEXT NOT NULL UNIQUE,
    `PKGSPEC`	  TEXT
)''')
        self.package.conn.execute('''INSERT INTO PORTS VALUES (
    "www/py-flask", "py-flask-*"
)''')
        self.package.conn.commit()

    def test_pkgspec_not_found(self):
        out = self.package._to_openbsd_fullpkgpath('py-requests')
        expected = 'xxx/py-requests'
        self.assertEqual(out, expected)

    def test_pkgspec_found(self):
        out = self.package._to_openbsd_fullpkgpath('py-flask')
        expected = 'www/py-flask'
        self.assertEqual(out, expected)

    def tearDown(self):
        self.package.conn.close()


class TestOpenBSDPackageLicenses(unittest.TestCase):
    def setUp(self):
        self.package = OpenBSDPackage()
        self.package.upt_pkg = upt.Package('foo', '42')

    def test_no_licenses(self):
        self.package.upt_pkg.licenses = []
        out = self.package._license_info()
        expected = '# TODO: check licenses\n'
        expected += 'PERMIT_PACKAGE_CDROM =\tXXX'
        self.assertEqual(out, expected)

    def test_one_license(self):
        self.package.upt_pkg.licenses = [upt.licenses.BSDThreeClauseLicense()]
        out = self.package._license_info()
        expected = '# BSD-3-Clause\n'
        expected += 'PERMIT_PACKAGE_CDROM =\tYes'
        self.assertEqual(out, expected)

    def test_bad_license(self):
        self.package.upt_pkg.licenses = [upt.licenses.UnknownLicense()]
        out = self.package._license_info()
        expected = '# unknown\n'
        expected += 'PERMIT_PACKAGE_CDROM =\tXXX'
        self.assertEqual(out, expected)

    def test_multiple_license(self):
        self.package.upt_pkg.licenses = [
            upt.licenses.BSDTwoClauseLicense(),
            upt.licenses.BSDThreeClauseLicense()
        ]
        out = self.package._license_info()
        expected = '# BSD-2-Clause\n# BSD-3-Clause\n'
        expected += 'PERMIT_PACKAGE_CDROM =\tYes'
        self.assertEqual(out, expected)


if __name__ == '__main__':
    unittest.main()
