# Copyright 2018      Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import logging
import os
import sqlite3
import sys

import jinja2
import upt


class OpenBSDPackage(object):
    SQLPORTS_DB = '/usr/local/share/sqlports'

    def __init__(self):
        try:
            self.conn = sqlite3.connect(self.SQLPORTS_DB)
        except sqlite3.OperationalError:
            self.conn = None

        self.logger = logging.getLogger('upt')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.conn is not None:
            self.conn.close()

    def _to_openbsd_fullpkgpath(self, name):
        if self.conn is not None:
            query = 'SELECT FULLPKGPATH FROM PORTS WHERE PKGSPEC=?'
            cursor = self.conn.execute(query, (f'{name}-*', ))
            result = cursor.fetchone()
            if result is not None:
                return result[0]

        # The database cannot be used, or we could not find the row we wanted.
        # Let's return something anyway, and let the maintainer fix this.
        return f'xxx/{name}'

    def _create_output_directories(self, upt_pkg, output_dir=None):
        """Creates the directory layout required to port upt_pkg.

        If output_dir is None, we use $PORTSDIR/mystuff/$frontend/$pkg just
        like PortGen.
        """
        if output_dir is None:
            portsdir = os.environ.get('PORTSDIR', '/usr/ports')
            dirname = self._normalized_openbsd_name(upt_pkg.name)
            output_dir = os.path.join(portsdir, 'mystuff',
                                      self.upt_pkg.frontend, dirname)
        self.logger.info(f'Creating the directory structure in {output_dir}')
        self.output_dir = output_dir
        try:
            os.makedirs(os.path.join(self.output_dir, 'pkg'))
        except PermissionError:
            sys.exit(f'Cannot create {self.output_dir}: permission denied.')
        except FileExistsError:
            sys.exit(f'Cannot create {self.output_dir}: already exists.')

    def create_package(self, upt_pkg, output):
        self.upt_pkg = upt_pkg
        self._create_output_directories(upt_pkg, output)
        self._create_makefile()
        self._create_distinfo()
        self._create_pkg_descr()
        self.logger.info(f'You still need to create '
                         f'{self.output_dir}/pkg/PLIST')

    def _render_makefile_template(self):
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('upt_openbsd', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        env.filters['reqformat'] = self.jinja2_reqformat
        template = env.get_template(self.template)
        return template.render(pkg=self)

    def _create_makefile(self):
        self.logger.info(f'Creating the Makefile')
        with open(os.path.join(self.output_dir, 'Makefile'), 'w',
                  encoding='utf-8') as f:
            f.write(self._render_makefile_template())

    def _create_distinfo(self):
        self.logger.info(f'Creating distinfo')
        try:
            archive = self.upt_pkg.get_archive()
            with open(os.path.join(self.output_dir, 'distinfo'), 'w',
                      encoding='utf-8') as f:
                f.write(f'SHA256 ({archive.filename}) = '
                        f'{archive.sha256_base64}\n')
                f.write(f'SIZE ({archive.filename}) = {archive.size}\n')
        except (upt.ArchiveUnavailable, upt.HashUnavailable):
            self.logger.error('Failed to create distinfo')

    def _create_pkg_descr(self):
        self.logger.info(f'Creating pkg/DESCR')
        with open(os.path.join(self.output_dir, 'pkg/DESCR'), 'w',
                  encoding='utf-8') as f:
            f.write(self.upt_pkg.description)

    def _summary(self):
        summary = self.upt_pkg.summary
        if summary.endswith('.') and not summary.endswith('etc.'):
            summary = summary[:-1]
        if summary.startswith('a ') or summary.startswith('A '):
            summary = summary[2:]
        if summary.startswith('an ') or summary.startswith('An '):
            summary = summary[3:]
        return f'{summary[:1].lower()}{summary[1:]}'

    def _depends(self, phase):
        return self.upt_pkg.requirements.get(phase, [])

    @property
    def build_depends(self):
        return self._depends('build')

    @property
    def run_depends(self):
        return self._depends('run')

    @property
    def test_depends(self):
        return self._depends('test')

    def _license_info(self):
        """Return a string containing license information.

        The returned string contains:
        - a comment describing the package licenses;
        - a line setting 'PERMIT_PACKAGE_CDROM' (set to 'Yes' when we are sure
          that the license is 'good', and to 'XXX' otherwise).
        """
        out = ''
        permit_package_cdrom = bool(self.upt_pkg.licenses)

        # Based on infrastructure/lib/OpenBSD/PortGen/License.pm, found in
        # the OpenBSD ports.
        good_licenses = (
            upt.licenses.GNUAfferoGeneralPublicLicenseThreeDotZero,
            upt.licenses.ApacheLicenseOneDotOne,
            upt.licenses.ApacheLicenseTwoDotZero,
            upt.licenses.ArtisticLicenseOneDotZero,
            upt.licenses.ArtisticLicenseTwoDotZero,
            upt.licenses.BSDTwoClauseLicense,
            upt.licenses.GNUGeneralPublicLicenseTwo,
            upt.licenses.GNUGeneralPublicLicenseThree,
            upt.licenses.GNULesserGeneralPublicLicenseTwoDotOne,
            upt.licenses.GNULesserGeneralPublicLicenseTwoDotOnePlus,
            upt.licenses.MITLicense,
            upt.licenses.BSDThreeClauseLicense,
            upt.licenses.PerlLicense,
            upt.licenses.RubyLicense,
            upt.licenses.QPublicLicenseOneDotZero,
            upt.licenses.ZlibLicense,
        )

        # First, a comment describing the package license(s).
        for license in self.upt_pkg.licenses:
            out += f'# {license.spdx_identifier}\n'
            permit_package_cdrom &= isinstance(license, good_licenses)

        if not out:
            out = '# TODO: check licenses\n'

        # Then, let's fill in PERMIT_PACKAGE_CDROM.
        if permit_package_cdrom:
            out += 'PERMIT_PACKAGE_CDROM =\tYes'
        else:
            # If no license info was returned by the frontend, or even if we
            # could not be 100% sure that the license was a "good" one, we
            # should not assume that PERMIT_PACKAGE_CDROM should be set to
            # 'No': instead, let's make sure the maintainer checks the license
            # themselves.
            out += 'PERMIT_PACKAGE_CDROM =\tXXX'

        return out

    def jinja2_reqformat(self, req, flavor=''):
        openbsd_name = self._normalized_openbsd_name(req.name)
        fullpkgpath = self._to_openbsd_fullpkgpath(openbsd_name)
        return f'{fullpkgpath}{flavor}'

    def _pkgname(self):
        """Return a valid PKGNAME for the Makefile."""
        raise NotImplementedError()

    def _distname(self):
        """Return a valid DISTNAME for the Makefile."""
        raise NotImplementedError()

    @staticmethod
    def _normalized_openbsd_name(name):
        """Return an OpenBSD-compatible version of a package name.

        The result of this function should be the same thing as the
        fullpkgpath, but without the leading "<category>/". For instance, the
        'requests' package in Python has 'www/py-requests' as its fullpkgpath,
        and _normalized_openbsd_name('requests') should return 'py-requests'.
        """
        raise NotImplementedError()


class OpenBSDPerlPackage(OpenBSDPackage):
    template = 'perl.mk'

    def _pkgname(self):
        return f'p5-${{DISTNAME}}'

    def _distname(self):
        name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{name}-${{VERSION}}'

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.replace('::', '-')
        return f'p5-{name}'


class OpenBSDPythonPackage(OpenBSDPackage):
    template = 'python.mk'

    def _pkgname(self):
        openbsd_name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{openbsd_name}-${{MODPY_EGG_VERSION}}'

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.lower()
        if name == 'py':
            return 'py-py'

        if name.startswith('python-'):
            name = name[7:]
        elif name.startswith('py-'):
            name = name[3:]
        elif name.startswith('py'):
            name = name[2:]
        return f'py-{name}'

    def _distname(self):
        return f'{self.upt_pkg.name}-${{MODPY_EGG_VERSION}}'

    def jinja2_reqformat(self, req):
        return super().jinja2_reqformat(req, flavor='${MODPY_FLAVOR}')


class OpenBSDRubyPackage(OpenBSDPackage):
    template = 'ruby.mk'

    def _pkgname(self):
        return f'ruby-${{DISTNAME}}'

    def _distname(self):
        name = self._normalized_openbsd_name(self.upt_pkg.name)
        return f'{name}-${{VERSION}}'

    def jinja2_reqformat(self, req):
        return super().jinja2_reqformat(req, flavor=',${MODRUBY_FLAVOR}')

    @staticmethod
    def _normalized_openbsd_name(name):
        name = name.lower()
        if not name.startswith('ruby-'):
            name = f'ruby-{name}'
        return name


class OpenBSD(upt.Backend):
    name = 'openbsd'

    def create_package(self, upt_pkg, output=None):
        pkg_classes = {
            'pypi': OpenBSDPythonPackage,
            'cpan': OpenBSDPerlPackage,
            'rubygems': OpenBSDRubyPackage,
        }

        try:
            pkg_cls = pkg_classes[upt_pkg.frontend]
        except KeyError:
            raise upt.UnhandledFrontendError(self.name, upt_pkg.frontend)

        with pkg_cls() as packager:
            packager.create_package(upt_pkg, output)
