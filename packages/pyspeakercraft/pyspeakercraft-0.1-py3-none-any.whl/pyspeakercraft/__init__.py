import functools
import logging
import math
import serial
import time
from functools import wraps
from threading import RLock
from construct import Struct, Const, Int8ub, Checksum, Flag, BitStruct, Padding, Container

name = "pyspeakercraft"
log = logging.getLogger(__name__)

#constants
TIMEOUT = 2
COMMAND_WINDOW_OPEN = 0x11
COMMAND_WINDOW_CLOSED = 0x13
COMMAND_DELIMITER = 0x55

RESPONSE_ID = 0x95
RESPONSE_ACK = 0x01

VOLUME_SET = 0x05
VOLUME_SCALE = list(range(0, 45)) + [46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,80]
VOLUME_SCALE_LENGTH = len(VOLUME_SCALE)

def calculate_actual_volume(volume):
    volume_percent = (100-volume) / 100.0
    index = int(volume_percent * VOLUME_SCALE_LENGTH)
    index = max(0, index-1)
    value = VOLUME_SCALE[index]
    log.debug("volume calculation: %s %s %s %s %s", VOLUME_SCALE_LENGTH, volume, volume_percent, index, value)
    return value

#command formatters
cmd_zone_on = Struct(
    "length" / Const(0x04, Int8ub),
    "id" / Const(0xA0, Int8ub),
    "zone" / Int8ub
)

cmd_zone_off = Struct(
    "length" / Const(0x04, Int8ub),
    "id" / Const(0xA1, Int8ub),
    "zone" / Int8ub
)

cmd_source = Struct(
    "length" / Const(0x05, Int8ub),
    "id" / Const(0xA3, Int8ub),
    "zone" / Int8ub,
    "source" / Int8ub
)

cmd_volume = Struct(
    "length" / Const(0x08, Int8ub),
    "id" / Const(0x57, Int8ub),
    "reserve1" / Const(0x00, Int8ub),
    "reserve2" / Const(0x00, Int8ub),
    "action" / Int8ub,
    "action_data" / Int8ub,
    "zone" / Int8ub
)

cmd_zone_status = Struct(
    "length" / Const(0x04, Int8ub),
    "id" / Const(0x69, Int8ub),
    "zone" / Int8ub
)

response_zone_status = Struct(
    "delimiter" / Int8ub,
    "length" / Int8ub,
    "id" / Int8ub,
    "zone" / Int8ub,
    "reserved" / Int8ub,
    "flags" / BitStruct(
        Padding(4),
        "party_master" / Flag,
        "party" / Flag,
        "power" / Flag,
        "mute" / Flag),
    "source" / Int8ub,
    "volume" / Int8ub,
    "bass" / Int8ub,
    "treble" / Int8ub,
    "volume_actual" / Int8ub,
    "checksum" / Int8ub
)

class SpeakercraftZone(object):
    def __init__(self, message: Container):
        self.id = message.zone
        self.source = message.source
        self.power = message.flags.power
        self.mute = message.flags.mute
        self.volume = message.volume
        self.volume_actual = message.volume_actual
        self.bass = message.bass
        self.treble = message.treble

    def __repr__(self):
        return "<SpeakercraftZone i:%s s:%s p:%s m:%s v:%s va:%s b:%s t:%s>" % (self.id, self.source, self.power, self.mute, self.volume, self.volume_actual, self.bass, self.treble)


def get_speakercraft(port_url):
    lock = RLock()

    def synchronized(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper

    class SpeakercraftSync(object):
        def __init__(self, port_url):
            self._port = serial.serial_for_url(port_url, do_not_open=True)
            self._port.baudrate = 57600
            self._port.stopbits = serial.STOPBITS_ONE
            self._port.bytesize = serial.EIGHTBITS
            self._port.parity = serial.PARITY_NONE
            self._port.timeout = TIMEOUT
            self._port.write_timeout = TIMEOUT
            self._port.open()

            self._zones = dict()
            self._zones_timestamp = 0


        def _seek(self, delimiter):
            bytes = self._port.read(1)
            log.debug("received: %s", bytes.hex())

            while len(bytes) == 0 or bytes[0] != delimiter:
                bytes = self._port.read(1)
                log.debug("received: %s", bytes.hex())

            return bytearray([delimiter])

        def _receive_message(self):
            buffer = self._seek(COMMAND_DELIMITER)
            buffer += self._port.read(1)
            length = buffer[1]-1
            log.debug("length: %s", length)

            buffer += self._port.read(length)
            log.debug("response: <%s>", buffer.hex())

            checksum = sum(buffer) % 256
            log.debug("checksum: <%s>", checksum)

            return (checksum == 0, buffer)


        def _send_command(self, request: bytearray):
            # prepend sync byte and append checksum bytes
            request = bytes([COMMAND_DELIMITER]) + request
            checksum = (sum(request) % 256)
            if(checksum != 0):
                checksum = 256 - checksum
            request = request + bytes([checksum])
            log.debug('sending <%s>', request.hex())

            #wait for command window to opened
            log.debug("waiting for command window")
            self._port.reset_output_buffer()
            self._port.reset_input_buffer()
            self._seek(COMMAND_WINDOW_OPEN)

            # send
            log.debug("transmitting command")
            self._port.write(request)
            self._port.flush()

            # receive
            log.debug("waiting for response")
            response = self._receive_message()
            if(response[0]):
                return response[1][4] == 1
            else:
                return False

        def _refresh_zone_status(self):
            log.debug("refreshing zone status")
            self._port.reset_output_buffer()
            self._port.reset_input_buffer()

            self._seek(COMMAND_WINDOW_CLOSED)

            for x in range(0,6):
                response = self._receive_message()[1]
                container = response_zone_status.parse(response)
                zone = SpeakercraftZone(container)
                self._zones[zone.id] = zone

            self._zones_timestamp = time.time()

        @synchronized
        def zone_status(self, zone: int):
            log.info("check zone status %s", zone)

            # update zone details if they are older than 5 seconds
            if(time.time() - self._zones_timestamp > 5):
                self._refresh_zone_status()

            return self._zones[zone]

        @synchronized
        def set_power(self, zone: int, power: bool):
            log.info("power change z:%s p:%s", zone, power)
            if(power):
                request = cmd_zone_on.build(dict(zone=zone))
            else:
                request = cmd_zone_off.build(dict(zone=zone))

            self._zones_timestamp = 0
            return self._send_command(request)

        @synchronized
        def set_volume(self, zone: int, volume: int):
            log.info("volume change z:%s p:%s", zone, volume)
            volume_actual = calculate_actual_volume(volume)
            request = cmd_volume.build(dict(zone=zone, action=VOLUME_SET, action_data=volume_actual))

            self._zones_timestamp = 0
            return self._send_command(request)

        @synchronized
        def set_source(self, zone: int, source: int):
            log.info("source change z:%s p:%s", zone, source)
            request = cmd_source.build(dict(zone=zone, source=source))

            self._zones_timestamp = 0
            return self._send_command(request)

    log.info("Connecting to MZC on port %s", port_url)
    return SpeakercraftSync(port_url)


if __name__ == '__main__':
    import time
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/tmp/myapp.log',
                        filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(console)
    logging.info("Init speakercraft")


    sc = get_speakercraft("/dev/ttyUSB0")
    print(sc.zone_status(0))
