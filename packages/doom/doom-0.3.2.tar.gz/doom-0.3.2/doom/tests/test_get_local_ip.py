#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import socket
import subprocess
import tempfile
import time

import geocoder
import mock
from six.moves import StringIO

from doom.sysinfo import get_local_ip


class TestCachedIP(object):

    def test_get_cached_ip(self):
        now = 1460174717.44
        local_ip = '123.456.789.12'

        temp_home = tempfile.mkdtemp()
        bp_path = os.path.join(temp_home, '.bash_profile')
        fd = open(bp_path, 'w')
        fd.write('LOCAL_IP=' + local_ip + '\n'
                 '#LOCAL_IP_WRITE_TIME=' + str(now) + '\n')
        fd.close()

        with mock.patch.object(get_local_ip, 'home', temp_home):
            (cached_ip, cached_timestamp) = get_local_ip.get_cached_ip()

        os.remove(bp_path)
        os.rmdir(temp_home)
        assert cached_ip == local_ip, cached_ip
        assert cached_timestamp == now, cached_timestamp

    def test_get_cached_ip_missing(self):
        temp_home = tempfile.mkdtemp()
        with mock.patch.object(get_local_ip, 'home', temp_home):
            (cached_ip, cached_timestamp) = get_local_ip.get_cached_ip()

        os.rmdir(temp_home)
        assert cached_ip is None, cached_ip
        assert cached_timestamp == float("-inf"), cached_timestamp

    def test_get_cached_ip_invalid(self):
        now = '1460174717.44'
        local_ip = '123.456.789.12b'

        now2 = '1460174718.44'
        local_ip2 = '234.567.891.011'

        temp_home = tempfile.mkdtemp()
        bp_path = os.path.join(temp_home, '.bash_profile')
        fd = open(bp_path, 'w')
        fd.write('LOCAL_IP=' + local_ip + '\n'
                 '#LOCAL_IP_WRITE_TIME=' + str(now) + '\n')
        fd.write('LOCAL_IP=' + local_ip2 + '\n'
                 '#LOCAL_IP_WRITE_TIME=' + str(now2) + '\n')
        fd.close()

        c = StringIO()

        with mock.patch.object(get_local_ip, 'home', temp_home):
            with mock.patch.object(get_local_ip.sys, 'stderr', c):
                (cached_ip, cached_timestamp) = get_local_ip.get_cached_ip()

        os.remove(bp_path)
        os.rmdir(temp_home)

        assert cached_ip == local_ip, cached_ip
        assert cached_timestamp == float("-inf"), cached_timestamp

        cval = c.getvalue()
        expected = 'get_local_ip found 2 matches for LOCAL_IP_WRITE_TIME.'
        assert cval == expected, cval

    def test_write_ip_no_xdg(self):
        now = time.time()
        local_ip = '123.456.789.12'

        temp_home = tempfile.mkdtemp()

        with mock.patch.object(get_local_ip, 'home', temp_home):
            rc = get_local_ip.write_ip(local_ip, use_config_xdf=True)

        assert rc is None
        bp_path = os.path.join(temp_home, '.bash_profile')
        xdg_dir = os.path.join(temp_home, '.config')
        # xdg_path = os.path.join(xdg_dir, 'local_ip')
        assert os.path.exists(bp_path)
        assert not os.path.exists(xdg_dir)
        fd = open(bp_path, 'r')
        content = fd.read().strip('\r\n ')
        fd.close()
        line1 = content.splitlines()[0]
        line2 = content.splitlines()[1]
        assert line1 == 'LOCAL_IP=' + local_ip, line1
        assert line2.startswith('#LOCAL_IP_WRITE_TIME=')
        stamp = float(line2.split('=')[-1])
        assert abs(stamp - now) <= 2, stamp

        # shutil.rmtree is scary on anything that could accidentally be $HOME,
        # do it more carefully
        os.remove(bp_path)
        os.rmdir(temp_home)

    def test_write_ip_xdg(self):
        now = time.time()
        local_ip = '123.456.789.12'

        temp_home = tempfile.mkdtemp()
        os.mkdir(os.path.join(temp_home, '.config'))

        with mock.patch.object(get_local_ip, 'home', temp_home):
            rc = get_local_ip.write_ip(local_ip, use_config_xdf=True)

        assert rc is None
        bp_path = os.path.join(temp_home, '.bash_profile')
        xdg_dir = os.path.join(temp_home, '.config')
        xdg_path = os.path.join(xdg_dir, 'local_ip')
        assert not os.path.exists(bp_path)
        assert os.path.exists(xdg_path)
        fd = open(xdg_path, 'r')
        content = fd.read().strip('\r\n ')
        fd.close()
        line1 = content.splitlines()[0]
        line2 = content.splitlines()[1]
        assert line1 == 'LOCAL_IP=' + local_ip, line1
        assert line2.startswith('#LOCAL_IP_WRITE_TIME=')
        stamp = float(line2.split('=')[-1])
        assert abs(stamp - now) <= 2, stamp

        shutil.rmtree(temp_home)  # TODO: this is potentially scary!


class TestGetIP(object):

    def test_get_ip_geocoder(self):
        myip = mock.Mock()
        myip.side_effect = socket.error()

        geoip = mock.Mock()
        geoip.return_value.ip = u'104.13.60.51'

        with mock.patch.object(geocoder, 'ip', geoip):
            ret = get_local_ip.get_ip()

        assert ret == u'104.13.60.51', ret

    def test_get_ip_urlopen(self):
        myip = mock.Mock()
        myip.side_effect = socket.error()

        geoip = mock.Mock()
        geoip.side_effect = socket.error()

        mock_urlopen = mock.Mock()
        mock_urlopen.return_value.read.return_value = u'104.13.60.50'

        with mock.patch.object(geocoder, 'ip', geoip):
            with mock.patch.object(get_local_ip, 'urlopen', mock_urlopen):
                ret = get_local_ip.get_ip()

        assert ret == u'104.13.60.50'

    def test_httpbin_get(self):
        urlopen = mock.Mock()
        urlopen.side_effect = IOError

        c = StringIO()

        with mock.patch.object(get_local_ip, 'urlopen', urlopen):
            with mock.patch.object(get_local_ip.sys, 'stderr', c):
                ret = get_local_ip._httpbin_get()

        assert ret is None, ret

        cv = c.getvalue()
        msg = ('page load http://httpbin.org/ip failed with exception '
               'message: \n')
        assert cv == msg, cv


def test_exclude_lan_ips():
    ret = get_local_ip.exclude_lan_ips(None)
    assert ret is None, ret

    ret = get_local_ip.exclude_lan_ips('192.168.0.68')
    assert ret is None, ret

    ret = get_local_ip.exclude_lan_ips('10.0.0.0')
    assert ret is None, ret

    ret = get_local_ip.exclude_lan_ips('97.155.foo.bar')
    assert ret == '97.155.foo.bar', ret


def test_identify_ip():
    content = '192.168.1.254'
    ret = get_local_ip.identify_ip(content)
    assert ret == content, ret

    content = 'foo 104.13.60.50bar'
    ret = get_local_ip.identify_ip(content)
    assert ret == '104.13.60.50', ret

    content = None
    ret = get_local_ip.identify_ip(content)
    assert ret is None, ret

    content = 'razmataz'
    ret = get_local_ip.identify_ip(content)
    assert ret is None, ret

    content = '104.13.60.50 192.168.1.254'

    c = StringIO()

    with mock.patch.object(get_local_ip.sys, 'stderr', c):
        ret = get_local_ip.identify_ip(content)

    assert ret is None, ret

    cv = c.getvalue()
    msg = "Ambiguous IP address results: ['104.13.60.50', '192.168.1.254']"
    assert cv == msg, cv


def test_script():
    # test that the script runs properly
    p = subprocess.Popen('get_local_ip',
                         close_fds=True,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    g = p.communicate()
    stdout = g[0].decode('utf-8').strip()

    expected = get_local_ip.main()
    assert stdout == expected
