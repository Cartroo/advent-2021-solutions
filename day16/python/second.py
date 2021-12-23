#!/usr/bin/env python3.10

import math
from sys import stdin

# For ease of debugging I'm going to actually use the string form of
# binary -- this is less efficient, but makes it much easier to track
# down issues given that this file format is deliberately obfuscated by
# not respecting byte or word boundaries.

class BinaryReaderExhaustedError(Exception):
    pass

class BinaryReader:

    def __init__(self, hexstr="", binstr=""):
        self.hexstr = hexstr
        self.read_offset = 0
        self.bit_buffer = binstr

    def __repr__(self):
        return f"BinaryReader(offset={self.read_offset}, hexstr={self.hexstr}, binstr={self.bit_buffer}"

    def get_bits(self, num_bits):
        missing_bits = max(0, num_bits - len(self.bit_buffer))
        if missing_bits > 0:
            consume_chars = (missing_bits - 1) // 4 + 1
            to_decode = self.hexstr[self.read_offset:self.read_offset + consume_chars]
            self.bit_buffer += "".join(f"{int(i, 16):04b}" for i in to_decode)
            if len(to_decode) != consume_chars:
                raise BinaryReaderExhaustedError
            self.read_offset += consume_chars
        to_ret = self.bit_buffer[:num_bits]
        self.bit_buffer = self.bit_buffer[num_bits:]
        return to_ret

    def get_int(self, num_bits):
        return int(self.get_bits(num_bits), 2)

class LiteralPacket:

    def __init__(self, reader):
        final_nybble = False
        value_nybbles = []
        while not final_nybble:
            final_nybble = (reader.get_bits(1) == "0")
            value_nybbles.append(reader.get_bits(4))
        self.value = int("".join(value_nybbles), 2)

    def __repr__(self):
        return f"LiteralPacket(value={self.value})"

    def get_value(self):
        return self.value

class OperatorPacket:

    OPERATIONS = {
        0: sum,
        1: math.prod,
        2: min,
        3: max,
        5: lambda values: 1 if values[0] > values[1] else 0,
        6: lambda values: 1 if values[0] < values[1] else 0,
        7: lambda values: 1 if values[0] == values[1] else 0
    }

    def __init__(self, type_id, reader):
        self.type_id = type_id
        if reader.get_bits(1) == "1":
            # Next 11 bits are number of sub-packets
            num_packets = reader.get_int(11)
            self.sub_packets = [decode_packet(reader) for i in range(num_packets)]
        else:
            # Next 15 bits are number of bits of sub-packets
            num_bits = reader.get_int(15)
            sub_reader = BinaryReader(binstr=reader.get_bits(num_bits))
            self.sub_packets = list(yield_packets(sub_reader))

    def __repr__(self):
        subs = (repr(i) for i in self.sub_packets)
        return f"OperatorPacket(type_id={self.type_id}, sub_packets=[{', '.join(subs)}])"

    def get_value(self):
        op = self.OPERATIONS[self.type_id]
        return op([i.get_value() for v, i in self.sub_packets])
            
def decode_packet(reader):
    version = reader.get_int(3)
    type_id = reader.get_int(3)
    if type_id == 4:
        return version, LiteralPacket(reader)
    else:
        return version, OperatorPacket(type_id, reader)

def yield_packets(reader):
    try:
        while True:
            yield decode_packet(reader)
    except BinaryReaderExhaustedError:
        pass

version, packet = decode_packet(BinaryReader(hexstr=stdin.readline().strip()))
print(f"Expression value={packet.get_value()}")
