#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import sys


def setup():
    from LbPlatformUtils.tests import utils
    utils.setup_all()


def teardown():
    from LbPlatformUtils.tests import utils
    utils.teardown_all()


def flags_for_arch(arch):
    from LbPlatformUtils.architectures import ARCH_DEFS
    return u'flags: %s' % u' '.join(ARCH_DEFS.get(arch, []))


def test_os_id_function_selection():
    import platform
    import LbPlatformUtils.inspect as PU

    platform._system = 'Linux'
    del sys.modules['LbPlatformUtils.inspect']
    import LbPlatformUtils.inspect as PU
    assert PU.os_id is PU._Linux_os

    platform._system = 'Darwin'
    del sys.modules['LbPlatformUtils.inspect']
    import LbPlatformUtils.inspect as PU
    assert PU.os_id is PU._Darwin_os

    platform._system = 'Windows'
    del sys.modules['LbPlatformUtils.inspect']
    import LbPlatformUtils.inspect as PU
    assert PU.os_id is PU._Windows_os

    platform._system = 'dummy'
    del sys.modules['LbPlatformUtils.inspect']
    import LbPlatformUtils.inspect as PU
    assert PU.os_id is PU._unknown_os

    del sys.modules['LbPlatformUtils.inspect']


def test_os_release_detection():
    import platform
    import LbPlatformUtils.inspect as PU
    mappings = [
        ('centos7', '''NAME="CentOS Linux"
VERSION="7 (Core)"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="7"
PRETTY_NAME="CentOS Linux 7 (Core)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="http://cern.ch/linux/"
BUG_REPORT_URL="http://cern.ch/linux/"

CENTOS_MANTISBT_PROJECT="CentOS-7"
CENTOS_MANTISBT_PROJECT_VERSION="7"
REDHAT_SUPPORT_PRODUCT="centos"
REDHAT_SUPPORT_PRODUCT_VERSION="7"

'''),
        ('ubuntu1804', '''NAME="Ubuntu"
VERSION="18.04.1 LTS (Bionic Beaver)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 18.04.1 LTS"
VERSION_ID="18.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=bionic
UBUNTU_CODENAME=bionic
'''),
        ('suse15', '''NAME="openSUSE Leap"
VERSION="15.0"
ID="opensuse-leap"
ID_LIKE="suse opensuse"
VERSION_ID="15.0"
PRETTY_NAME="openSUSE Leap 15.0"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:opensuse:leap:15.0"
BUG_REPORT_URL="https://bugs.opensuse.org"
HOME_URL="https://www.opensuse.org/"
'''),
        ('sl7', '''NAME="Scientific Linux"
VERSION="7.5 (Nitrogen)"
ID="rhel"
ID_LIKE="scientific centos fedora"
VERSION_ID="7.5"
PRETTY_NAME="Scientific Linux 7.5 (Nitrogen)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:scientificlinux:scientificlinux:7.5:GA"
HOME_URL="http://www.scientificlinux.org//"
BUG_REPORT_URL="mailto:scientific-linux-devel@listserv.fnal.gov"

REDHAT_BUGZILLA_PRODUCT="Scientific Linux 7"
REDHAT_BUGZILLA_PRODUCT_VERSION=7.5
REDHAT_SUPPORT_PRODUCT="Scientific Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="7.5"'''),
        # this one is a guess
        ('redhat7', '''ID="rhel"
VERSION_ID="7.5"'''),
    ]

    for expected, os_release in mappings:
        assert PU.parse_os_release(os_release.splitlines(True)) == expected, \
            'tested os-release did not map to %s' % expected

    try:
        PU.parse_os_release(['ID=super-distro', 'VERSION_ID=1.0'])
        assert False, 'ValueError exception expected'
    except ValueError:
        pass


def test_rh_flavours():
    import platform
    import LbPlatformUtils.inspect as PU

    mappings = [
        # RHEL 7 equivalent
        (('centos', '7.4.1708', 'Core'),
         ('/etc/centos-release', 'CentOS Linux release 7.4.1708 (Core)\n'),
         'centos7'),
        (('redhat', '7.4.1708', 'Core'),
         ('/etc/redhat-release', 'Scientific Linux SL release 7.x\n'),
         'sl7'),
        (('redhat', '7.4.1708', 'Core'),
         ('/etc/redhat-release', 'Redhat Enterprise Linux release 7.x\n'),
         'redhat7'),

        # RHEL 6 equivalent
        (('centos', '6.9', 'Core'),
         ('/etc/centos-release', 'CentOS Linux release 6.x (Core)\n'),
         'centos6'),
        (('redhat', '6.9', 'Core'),
         ('/etc/redhat-release', 'Scientific Linux SL release 6.x\n'),
         'sl6'),
        (('redhat', '6.9', 'Core'),
         ('/etc/redhat-release', 'Scientific Linux CERN SLC release 6.x\n'),
         'slc6'),
        (('redhat', '6.9', 'Core'),
         ('/etc/redhat-release', 'Redhat Enterprise Linux release 6.x\n'),
         'redhat6'),

        # RHEL 7 equivalent
        (('centos', '5.0', 'X'),
         ('/etc/centos-release', 'CentOS Linux release 5.x (Core)\n'),
         'centos5'),
        (('redhat', '5.11', 'Boron'),
         ('/etc/redhat-release', 'Scientific Linux SL release 5.x\n'),
         'sl5'),
        (('redhat', '5.11', 'Boron'),
         ('/etc/redhat-release', 'Scientific Linux CERN SLC release 5.x\n'),
         'slc5'),
        (('redhat', '5.11', 'Boron'),
         ('/etc/redhat-release', 'Redhat Enterprise Linux release 5.x\n'),
         'redhat5'),
    ]

    for platform._linux_dist_short, (relname, reldata), expected in mappings:
        open._overrides[relname] = reldata
        open._overrides['/etc/os-release'] = None
        assert PU._Linux_os() == expected, \
            '%s did not map to %s' % (reldata.strip(), expected)


def test_suse():
    import platform
    import LbPlatformUtils.inspect as PU

    mappings = [
        (('suse', '9.9.9', 'xyz'), 'suse9'),
    ]

    for platform._linux_dist_short, expected in mappings:
        assert PU._Linux_os() == expected, \
            '%s did not map to %s' % (platform._linux_dist_short, expected)


def test_debian_flavours():
    import platform
    import LbPlatformUtils.inspect as PU

    mappings = [
        # Ubuntu (native)
        (('Ubuntu', '16.04', 'xenial'),
         ('/etc/lsb-release', 'DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=16.04\n'),
         'ubuntu1604'),
        (('Ubuntu', '18.04', 'bionic'),
         ('/etc/lsb-release', 'DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=18.04\n'),
         'ubuntu1804'),

        # Ubuntu (vanilla Python)
        (('debian', 'stretch/sid', ''),
         ('/etc/lsb-release', 'DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=16.04\n'),
         'ubuntu1604'),
        (('debian', 'jessie/sid', ''),
         ('/etc/lsb-release', 'DISTRIB_ID=Ubuntu\nDISTRIB_RELEASE=18.04\n'),
         'ubuntu1804'),

        # Debian
        (('debian', '9.3', ''),
         ('/etc/lsb-release', None),
         'debian9'),
        (('debian', '8.10', ''),
         ('/etc/lsb-release', None),
         'debian8'),
        (('debian', '7.11', ''),
         ('/etc/lsb-release', None),
         'debian7'),

        # Unknown by Python platform module
        (('', '', ''),
         ('/etc/lsb-release', None),
         'linux'),
    ]

    for platform._linux_dist_short, (relname, reldata), expected in mappings:
        open._overrides[relname] = reldata
        assert PU._Linux_os() == expected, \
            '%s did not map to %s' % (platform._linux_dist_short, expected)


def test_macos():
    import platform
    import LbPlatformUtils.inspect as PU

    mappings = [
        (('10.10.5', ('', '', ''), 'x86_64'), 'macos1010'),
    ]

    for platform._linux_dist_short, expected in mappings:
        assert PU._Darwin_os() == expected


def test_windows():
    import platform
    import LbPlatformUtils.inspect as PU

    mappings = [
        (('8', '6.2.9200', '', 'Multiprocessor Free'), 'win6'),
        (('10', '10.0.10240', '', 'Multiprocessor Free'), 'win10'),
    ]

    for platform._linux_dist_short, expected in mappings:
        assert PU._Windows_os() == expected


def test_unknown_os():
    import platform
    import LbPlatformUtils.inspect as PU

    assert PU._unknown_os() == 'unknown'


def test_host_os():
    import platform
    import LbPlatformUtils as PU
    import LbPlatformUtils.inspect as PUI
    from LbPlatformUtils.inspect import os_id as orig_os_id

    from contextlib import contextmanager

    @contextmanager
    def force_os_id(name):
        PUI.os_id = lambda: name
        yield
        PUI.os_id = orig_os_id

    mappings = [
        ('x86_64', ('debian8', 'Linux', flags_for_arch('x86_64')),
         'x86_64-debian8'),
        ('', ('slc6', 'Linux', 'nothing'),
         'unknown-slc6'),
        ('x86_64', ('slc6', 'Linux', flags_for_arch('x86_64')),
         'x86_64-slc6'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('haswell')),
         'haswell-centos7'),
        ('x86_64', ('suse42', 'Linux', 'nothing'),
         'x86_64-centos7'),
    ]
    for platform._machine, \
            (os_id, platform._system, open._overrides['/proc/cpuinfo']), \
            expected in mappings:
        with force_os_id(os_id):
            detected = PU.host_os()
            assert detected == expected


def test_microarch_flags():
    import LbPlatformUtils.inspect as PUI
    open._overrides['/proc/cpuinfo'] = 'flags           : sse2 sse4_2 abc xyz'
    assert PUI.microarch_flags() == set('sse2 sse4_2 abc xyz'.split())

    open._overrides['/proc/cpuinfo'] = 'nothing'
    assert PUI.microarch_flags() == set()

    open._overrides['/proc/cpuinfo'] = None
    assert PUI.microarch_flags() == set()


def test_model_name():
    import LbPlatformUtils.inspect as PUI
    expected = 'Intel(R) Core(TM) i7-7560U CPU @ 2.40GHz'
    open._overrides['/proc/cpuinfo'] = 'model name      : ' + expected
    assert PUI.model_name() == expected

    open._overrides['/proc/cpuinfo'] = 'nothing'
    assert PUI.model_name() == 'unknown'

    open._overrides['/proc/cpuinfo'] = None
    assert PUI.model_name() == 'unknown'


def test_dirac_platform():
    import platform
    import LbPlatformUtils.inspect as PUI
    from LbPlatformUtils.inspect import os_id as orig_os_id

    from contextlib import contextmanager

    @contextmanager
    def force_os_id(name):
        PUI.os_id = lambda: name
        # this is to make sure dirac_platform does not remember the old os_id
        del sys.modules['LbPlatformUtils']
        yield
        PUI.os_id = orig_os_id

    mappings = [
        ('x86_64', ('debian8', 'Linux', flags_for_arch('x86_64')),
         'x86_64-unknown'),
        ('', ('slc6', 'Linux', 'dummy'),
         'unknown-slc6'),
        ('x86_64', ('slc6', 'Linux', flags_for_arch('x86_64')),
         'x86_64-slc6'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('core2')),
         'core2-centos7'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('nehalem') + ' abc xyz'),
         'nehalem-centos7'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('sandybridge')),
         'sandybridge-centos7'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('sandybridge') + ' avx2'),
         'sandybridge-centos7'),
        ('x86_64', ('centos7', 'Linux', flags_for_arch('haswell')),
         'haswell-centos7'),
        ('x86_64', ('suse42', 'Linux', flags_for_arch('x86_64')),
         'x86_64-centos7'),
        ('x86_64', ('redhat6', 'Linux', flags_for_arch('x86_64')),
         'x86_64-slc6'),
        ('x86_64', ('slc5', 'NoLinux', None),
         'x86_64-slc5'),
        ('i386', ('slc5', 'NoLinux', None),
         'i386-slc5'),
        ('i686', ('slc5', 'NoLinux', None),
         'i686-slc5'),
    ]
    for platform._machine, \
            (os_id, platform._system, open._overrides['/proc/cpuinfo']), \
            expected in mappings:
        with force_os_id(os_id):
            import LbPlatformUtils as PU
            detected = PU.dirac_platform()
            assert detected == expected


def test_compiler_id():
    import subprocess
    if 'LbPlatformUtils.inspect' in sys.modules:
        del sys.modules['LbPlatformUtils.inspect']
    import LbPlatformUtils
    import LbPlatformUtils.inspect as PUI

    from contextlib import contextmanager

    @contextmanager
    def override_check_output(stdout, stderr, returncode):
        def mock_check_output(*args, **kwargs):
            if returncode:
                raise subprocess.CalledProcessError(returncode, args[0])
            if kwargs.get('stderr') == subprocess.STDOUT:
                return (stdout + stderr).encode('utf-8')
            return stdout.encode('utf-8')
        check_output_orig = PUI.check_output
        PUI.check_output = mock_check_output
        yield
        PUI.check_output = check_output_orig

    mappings = [
        (('',
          'blah\nThread model: posix\n'
          'gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.6)',
          0), 'gcc54'),
        (('',
          'blah\nThread model: posix\n'
          'gcc version 4.4.7 20120313 (Red Hat 4.4.7-18) (GCC)',
          0), 'gcc44'),
        (('',
          'blah\nThread model: posix\n'
          'gcc version 4.8.5 20150623 (Red Hat 4.8.5-16) (GCC)',
          0), 'gcc48'),
        (('',
          'blah\nThread model: posix\n'
          'gcc version 6.2.0 (GCC)',
          0), 'gcc62'),
        (('',
          'blah\nThread model: posix\n'
          'gcc version 7.3.0 (GCC)',
          0), 'gcc7'),
        (('',
          'clang version 5.0.0 (trunk 296300)\n'
          'Target: x86_64-unknown-linux-gnu',
          0), 'clang50'),
        (('',
          'icc version 18.0.0 (gcc version 4.4.7 compatibility)\n',
          0), 'icc18'),
        (('',
          'new fancy stuff 10.0\n',
          0), 'unknown'),
        (('',
          '-bash: cc: command not found\n',
          127), 'unknown')
    ]
    for (stdout, stderr, returncode), expected in mappings:
        with override_check_output(stdout, stderr, returncode):
            assert PUI.compiler_id() == expected
