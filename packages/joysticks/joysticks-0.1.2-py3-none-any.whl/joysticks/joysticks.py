#!/usr/bin/env python
import struct

def main():
    struct_format = 'llHHI'
    infile_path = "/dev/input/js0"
    infile = open(infile_path, "rb")
    event_size = struct.calcsize(struct_format)
    while True:
        event = infile.read(event_size)
        data = struct.unpack(struct_format, event)
        print(data)
        # (tv_sec, tv_usec, etype, code, value) = data
