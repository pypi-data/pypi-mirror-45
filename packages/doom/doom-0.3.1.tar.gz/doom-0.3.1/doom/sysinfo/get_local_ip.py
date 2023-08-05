#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
get_local_ip wraps several different implementations of IP-finding,
including geocoder and queries to e.g. "http://httpbin.org/ip".

The distinguishing feature of get_local_ip is that the results are
cached in .bash_profile, along with a timestamp of the last time the
IP was checked.  At runtime, get_local_ip will check to see if the
computer has been restarted or put into "sleep" move more recently
than the last cached timestamp.  If so, it will consider the cache
invalid and re-check.  Otherwise it will use the cached value.

This is intended to make get_local_ip network-friendly for running
at the beginning of many processes.
"""
import os
import re
import sys
import time

from six.moves.urllib.request import urlopen
import psutil

home = os.path.expanduser('~')
cache_invalidation_param = 24 * 3600


def get_cached_ip():
    """
    After checking this computer's IP address from an online source, it will
    be cached in .bash_profile.  For the purposes of cache invalidation, a
    comment will be included with a timestamp.  get_cached_ip checks for
    this cached IP and timestamp.

    cache_timestamp should be either None or a unix timestamp.  This is
    preferable to a datetime.datetime object because the latter do not compare
    well with other types.

    Returns
    -------
    cached_ip : str or None
    cache_timestmap : float or None
        unix timestamp, -inf if no timestamp is indentified
    """
    (cached_ip, cache_timestamp) = (None, float("-inf"))

    # Defining these here makes it easier to mock
    bash_profile_path = os.path.join(home, '.bash_profile')
    xdg_dir = os.path.join(home, '.config')
    xdg_path = os.path.join(xdg_dir, 'local_ip')

    if os.path.exists(xdg_path):
        with open(xdg_path, 'r') as fd:
            content = fd.read()

    elif os.path.exists(bash_profile_path):
        with open(bash_profile_path, 'r') as fd:
            content = fd.read()

    else:
        content = u''

    match = re.search('LOCAL_IP=.*', content)
    if match:
        cached_ip = match.group().split('=')[-1]

    matches = re.findall(r'#LOCAL_IP_WRITE_TIME=(?P<wt>[0-9\.]*)', content)
    if not matches:
        pass
    elif len(matches) > 1:
        sys.stderr.write('get_local_ip found {nmatches} matches '
                         'for LOCAL_IP_WRITE_TIME.'
                         .format(nmatches=len(matches)))
    else:
        match = matches[0]
        cache_timestamp = match.split('=')[-1]
        cache_timestamp = float(cache_timestamp)

    return (cached_ip, cache_timestamp)


def write_ip(local_ip, use_config_xdf=True):
    """
    Cache the value local_ip in .bash_profile, erasing any invalidated cached
    values that are already there.  Write alongside the new value a comment
    with the unix timestamp at which this new cached value is written.

    If config_xdg is True, then write this cached value to ~/.config/local_ip
    instead of to ~/.bash_profile.

    Parameters
    ----------
    local_ip : str
    use_config_xdf : bool, default True
    """
    # Defining these here makes them easier to mock.
    bash_profile_path = os.path.join(home, '.bash_profile')
    xdg_dir = os.path.join(home, '.config')

    if use_config_xdf and os.path.exists(xdg_dir):
        xdg_path = os.path.join(xdg_dir, 'local_ip')
        now = int(time.time())
        with open(xdg_path, 'w') as fd:
            fd.write('LOCAL_IP=%s\n#LOCAL_IP_WRITE_TIME=%s\n' %
                     (local_ip, now))

    else:
        fd = open(bash_profile_path, 'a')  # Touch the file
        fd.close()
        with open(bash_profile_path, 'r') as fd:
            content = fd.read().strip()

        content = re.sub('LOCAL_IP=[^\n]*', '', content).strip('\n')
        content = re.sub(r'#LOCAL_IP_WRITE_TIME=\d*(\.\d*)?', '', content)
        content = content.strip('\n')
        now = int(time.time())
        content = (content + '\n' +
                   'LOCAL_IP=%s\n#LOCAL_IP_WRITE_TIME=%s\n' % (local_ip, now,))

        with open(bash_profile_path, 'w') as fd:
            fd.write(content)
    return


# -------------------------------------------------------------------------

def get_ip():
    """
    Check one of several online APIs to find this computer's IP address,
    falling back to the next option if any given API fails.  A warning is
    issued only if all API's fail*.

    * This should probably be changed, as it is not likely to
    "degrade gracefully."

    # Alternatives:
    # http://whatismyipaddress.com/
    # http://www.ip-tracker.org/

    Returns
    -------
    local_ip : str or None
    """
    local_ip = _geocoder_get()

    if local_ip is None:
        local_ip = _httpbin_get()

    return local_ip


def _geocoder_get():
    try:
        # lazy import, since this imports requests, which on raspi takes over
        #  4 seconds
        import geocoder
    except ImportError:
        return None

    local_ip = None
    try:
        g = geocoder.ip('me')
        gip = g.ip
    except Exception:
        gip = None
    else:
        local_ip = identify_ip(gip)
        local_ip = exclude_lan_ips(local_ip)
    return local_ip


def _httpbin_get():
    local_ip = None
    try:
        page = urlopen('http://httpbin.org/ip')
        content = page.read()
        page.close()
    except Exception:
        exc = sys.exc_info()
        content = None
        sys.stderr.write('page load http://httpbin.org/ip failed with '
                         'exception message: %s\n' % exc[1])
    else:
        local_ip = identify_ip(content)
        local_ip = exclude_lan_ips(local_ip)
    return local_ip


# -------------------------------------------------------------------------
# IP Identification

def exclude_lan_ips(local_ip):
    """
    Given a candidate that may be a Public IP address, check that it is not
    a LAN IP address.  If it is not a LAN IP address, return the input
    unchanged.  Otherwise return None.

    Parameters
    ----------
    local_ip : unicode or None

    Returns
    -------
    local_ip : unicode or None
    """
    # 2016-05-15 got a result 192.168.0.255, LAN IP instead
    # of public IP.
    if isinstance(local_ip, bytes):
        local_ip = local_ip.decode('utf-8')

    if local_ip is None:
        pass
    elif local_ip.startswith('192.168.'):
        # This is an address on the local LAN
        local_ip = None
    elif local_ip in ['10.0.0.0', '8.8.8.8']:
        # 10.0 is another LAN address I think
        # 8.8.8.8 is Google DNS server, which was incorrectly
        # returned 2018-05-28 for reasons unknown
        local_ip = None
    else:
        pass
    return local_ip


def identify_ip(content):
    """
    Try to identify an IPv4 address in the given content.

    * Unhandled * IPv6, which geocoder sometimes returns.

    Parameters
    ----------
    content : str

    Returns
    -------
    ip : str or None
    """
    if not content:
        matches = []
    elif isinstance(content, bytes):
        matches = re.findall(br'\d+\.\d+\.\d+\.\d+', content)
    else:
        matches = re.findall(r'\d+\.\d+\.\d+\.\d+', content)
    matches = list(set(matches))

    ip = None
    if len(matches) == 1:
        ip = matches[0]
    elif len(matches) > 1:
        matches = sorted(matches)
        sys.stderr.write('Ambiguous IP address results: %s' % matches)

    return ip


# -------------------------------------------------------------------------

def main():
    """
    Find the cached IP address and the timestamp when that cache was written,
    if such exists.

    If the computer has been restarted or put in sleep mode more recently than
    this timestamp, the computer may have been moved (e.g. laptop sleep) and
    the cached value is considered invalidated.

    If the cache is not invalidated, return the cached value.  Otherwise, use
    one of several online tools to find the IP address.  Then write a new
    cache and cache timestamp to .bash_profile.

    Returns
    -------
    local_ip : str or None
    """
    now = time.time()
    (cached_ip, cache_timestamp) = get_cached_ip()
    local_ip = cached_ip
    last_restart = psutil.boot_time()

    # TODO: if/when psutil implements last_sleep_time, invalidate the
    #  cache at the last time the computer was put to sleep;
    #  see https://github.com/giampaolo/psutil/issues/1468
    last_sleep = -float('inf')

    validation_cutoff = max(last_sleep, last_restart)

    if cache_timestamp is None:
        # No cached IP found.
        pass
    elif cache_timestamp + cache_invalidation_param < now:
        # Because some ISPs may assign dynamic IPs, re-check after a while
        # (cache invalidation param defaults to 1 day as of 2015-12-15)
        # even if other criteria suggest the cache should remain valid.
        pass
    elif cached_ip and validation_cutoff < cache_timestamp:
        return cached_ip

    local_ip = get_ip()
    if cached_ip and not local_ip:
        return cached_ip
    elif not local_ip:
        return None

    write_ip(local_ip)
    return local_ip


def script():  # pragma: no cover
    # "no cover" because this is tested by test_get_local_ip.test_script
    #  but the code actually executed by that test is the version installed
    #  in site-packages, which is not reported
    # entry_point as specified by setup.py
    local_ip = main()
    if local_ip:
        print(local_ip)
        sys.exit(0)
    sys.exit(1)
