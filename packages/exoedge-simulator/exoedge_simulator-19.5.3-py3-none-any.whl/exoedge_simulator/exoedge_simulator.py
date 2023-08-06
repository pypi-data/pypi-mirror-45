# pylint: disable=C0103,W1202
""" Sample ExoEdge application

This module provides utilities for simulating data to enable a quick-start
experience with ExoEdge and the IIoT solution ExoSense.
"""
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import time as _time
import random
import threading
import math
import json
import re
import socket
import fcntl
import struct
import platform as _platform
import subprocess
import traceback
from builtins import bytes
from exoedge.sources import ExoEdgeSource
from exoedge import logger
from exoedge.sources.waves import *

LOG = logger.getLogger(__name__)

try:
    from sys_info import *
except ImportError:
    LOG.warning("Unable to import psutil. Please install in order to use the sys_info ExoEdge source.")

#Have args,kwargs so generic function call with superfluous parameters in config_io play nicely
def fourteen(*args, **kwargs):
    """ Return 14 """
    return 14

#Have args,kwargs so generic function call with superfluous parameters in config_io play nicely
def current_time(*args, **kwargs):
    """ Return the current timestamp """
    return _time.time()


def echo(*args, **kwargs):
    """ Echo a value into a string

    Parameters:
    value:          The value to be echoed
    """
    value=kwargs.get('value', "Hello World")
    return value


def strip_non_numeric(*args, **kwargs):
    """ Strip out non-numeric characters from string

    Parameters:
    value:          The value to be stripped to numeric values
    """
    value=kwargs.get('value', "1234BEEF")
    return int(re.sub('[^0-9]', '', value))


def sin_wave(*args, **kwargs):
    """ Generate a sin wave from the current time

    Parameters:
    period:         The period, in seconds, of the sin wave
    amplitude:      The amplitude of the sin wave
    offset:         The vertical offset of the sin wave
    """
    period=kwargs.get('period', 60)
    amplitude=kwargs.get('amplitude', 1)
    offset=kwargs.get('offset', 0)
    precision=kwargs.get('precision', 2)

    ratio = (_time.time() % period) / period
    return round(math.sin(2 * math.pi * ratio) * amplitude + offset, precision)


def cos_wave(*args, **kwargs):
    """ Generate a sin wave from the current time

    Parameters:
    period:         The period, in seconds, of the cos wave
    amplitude:      The amplitude of the cos wave
    offset:         The vertical offset of the cos wave
    """
    period=kwargs.get('period', 60)
    amplitude=kwargs.get('amplitude', 1)
    offset=kwargs.get('offset', 0)
    precision=kwargs.get('precision', 2)

    ratio = (_time.time() % period) / period
    return round(math.cos(2 * math.pi * ratio) * amplitude + offset, precision)


def location(*args, **kwargs):
    """ Generate location data from the current time and a starting location

    Moves in a circle every `period` seconds. Path is `radius` decimal degrees
    from the center point defined by `latitude` and `longitude`.

    Parameters:
    latitude:       The latitude of the center point, in decimal degrees
    longitude:      The longitude of the center point, in decimal degrees
    period:         The period, in seconds, it takes to traverse the path
    radius:         The radius, in decimal degrees, of the path from the center
    """
    latitude=kwargs.get('latitude', None)
    longitude=kwargs.get('longitude', None)
    period=kwargs.get('period', 60)
    radius=kwargs.get('radius', 0.1)
    precision=kwargs.get('precision', 6)

    lat = sin_wave(period=period,
                   amplitude=radius,
                   offset=latitude,
                   precision=precision)
    lng = cos_wave(period=period,
                   amplitude=radius,
                   offset=longitude,
                   precision=precision)
    return json.dumps({'lat': lat, 'lng': lng})


def random_integer(*args, **kwargs):
    """ Get a random integer between two values

    Parameters:
    lower:          The lower bound of the random number
    upper:          The upper bound of the random number
    """
    lower=kwargs.get('lower', 0)
    upper=kwargs.get('upper', 10)

    return random.randint(lower, upper)

def random_sleep_2(*args, **kwargs):
    """ Sleep for a random number of seconds

    Distinct from random_sleep_1 in that there is no additional thread
    required to get a value into the Channel. Instead, it merely returns when
    the sleep is done.

    Parameters:
    lower:          The lower bound of the sleep time, in seconds
    upper:          The upper bound of the sleep time, in seconds
    """
    lower=kwargs.get('lower', 0)
    upper=kwargs.get('upper', 10)

    r = random.randint(lower, upper)
    LOG.info('sleeping %ss', r)
    _time.sleep(r)
    return current_time()

def ip_address(*args, **kwargs):
    """ Returns a string that represents the ip address
        in octet form of the iface parameter given.
        Example:
            $ print(ip_address('eth0'))
            '192.168.1.100'

    """
    interface=kwargs.get('interface', '')
    interface = bytes(interface, 'ascii')
    LOG.info("ip_address: finding ip address for interface: {!r}".format(interface))
    ipaddress = None
    if _platform.system() == 'Darwin':
        try:
            import netifaces
        except ImportError:
            ipaddress = 'ip_address: Cannot run on Darwin unless "netiface" module is installed.'
        addrs = netifaces.ifaddresses(interface)
        ipaddress = [addr.get('addr') for addr in addrs[netifaces.AF_INET]]
        LOG.debug("On darwin, found IP addresses for '{}': {}"
                  .format(interface, ipaddress))
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ipaddress = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', interface[:15]))[20:24])
        except IOError as err:
            if err.errno == 19:
                msg = "ip_address: {0} not configured.".format(interface)
                ipaddress = msg
                LOG.warning(msg)
            elif err.errno == 99:
                msg = "ip_address: {0} not connected.".format(interface)
                ipaddress = msg
                LOG.error(msg)
            else:
                msg = "ip_address: {!r}: {!r}".format(interface, err)
                ipaddress = msg
                LOG.error(msg)
                LOG.critical(msg, exc_info=True)
    return ipaddress

class SimulatorExoEdgeSource(ExoEdgeSource):

    def run(self):

        while not self.is_stopped():
            for channel in self.get_channels_by_application("Simulator"): 
                if channel.is_sample_time():
                    LOG.warning("sample_time for: {}".format(channel.name))
                    func = channel.protocol_config.app_specific_config['function']
                    if sys.modules.get(__name__) and hasattr(sys.modules[__name__], func):
                        function = getattr(sys.modules[__name__], func)
                        par = channel.protocol_config.app_specific_config['parameters']
                        pos = channel.protocol_config.app_specific_config['positionals']
                        LOG.warning("calling '{}' with: **({})"
                                    .format(function, par))
                        try:
                            channel.put_sample(function(*pos, **par))
                        except Exception as exc: # pylint: disable=W0703
                            LOG.exception("Exception".format(format_exc=exc))
                            channel.put_channel_error(traceback.format_exc(exc))

                    else:
                        channel.put_channel_error(
                            'ExoSimulator has no function: {}'.format(func))

            _time.sleep(0.1)

        LOG.critical("ExoSimulator EXITING!")

