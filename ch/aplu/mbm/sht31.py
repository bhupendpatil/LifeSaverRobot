# sht31.py
# Sensirion temperature/humidity sensor
# Version 1.00 - Dec. 5, 2018

from calliope_mini import i2c, sleep

_R_HIGH   = 1
_R_MEDIUM = 2
_R_LOW    = 3

class SHT31:
    _map_cs_r = {
        True: {
            _R_HIGH : b'\x2c\x06',
            _R_MEDIUM : b'\x2c\x0d',
            _R_LOW: b'\x2c\x10'
            },
        False: {
            _R_HIGH : b'\x24\x00',
            _R_MEDIUM : b'\x24\x0b',
            _R_LOW: b'\x24\x16'
            }
        }

    def __init__(self, addr = 0x44):
        self._addr = addr

    def _send(self, buf):
        i2c.write(self._addr, buf)

    def _recv(self, count):
        return i2c.read(self._addr, count)

    def _raw_temp_humi(self, r = _R_HIGH, cs = True):
        """
        Read the raw temperature and humidity from the sensor and skips CRC
        checking.
        Returns a tuple for both values in that order.
        """
        if r not in (_R_HIGH, _R_MEDIUM, _R_LOW):
            raise ValueError('Wrong repeatabillity value given!')
        self._send(self._map_cs_r[cs][r])
        sleep(50)
        raw = self._recv(6)
        return (raw[0] << 8) + raw[1], (raw[3] << 8) + raw[4]

    def get_temp_humi(self, resolution = _R_HIGH, clock_stretch = True, celsius = True):
        """
        Read the temperature in degree celsius or fahrenheit and relative
        humidity. Resolution and clock stretching can be specified.
        Returns a tuple for both values in that order.
        """
        t, h = self._raw_temp_humi(resolution, clock_stretch)
        if celsius:
            temp = -45 + (175 * (t / 65535))
        else:
            temp = -49 + (315 * (t / 65535))
        return temp, 100 * (h / 65535)
