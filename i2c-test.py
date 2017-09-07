#!/usr/bin/env python
# encoding: utf-8
"""
Created by Peter Huewe on 2009-10-26.
Copyright 2009 Peter Huewe <peterhuewe@gmx.de>
Based on the spi testscript from Sean Nelson

This file is part of pyBusPirate.

pyBusPirate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBusPirate is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyBusPirate.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys
import argparse
import serial
import time
import crcmod
from pyBusPirateLite.I2C import *
""" enter binary mode """

def enter_in_i2c_mode(port):
    port.write("m\n")
    time.sleep(0.1)
    port.write("4\n")
    time.sleep(0.1)
    port.write("1\n")
    port.flushInput()
    time.sleep(0.1)

def i2c_write_data(data):
    i2c.send_start_bit()
    i2c.bulk_trans(len(data),data)
    i2c.send_stop_bit()


def i2c_read_bytes(address, numbytes, ret=False):
    data_out=[]
    i2c.send_start_bit()
    i2c.bulk_trans(len(address),address)
    while numbytes > 0:
        if not ret:
            print ord(i2c.read_byte())
        else:
            data_out.append(ord(i2c.read_byte()))
        if numbytes > 1:
            i2c.send_ack()
        numbytes-=1
    i2c.send_nack()
    i2c.send_stop_bit()
    if ret:
        return data_out

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("port", help="Specify connection port.")
    parser.add_argument("device", help="Device address.", type=lambda x: int(x,0))
    parser.add_argument("register", help="Register address.", type=lambda x: int(x,0))
    parser.add_argument("bytes", help="Number of bytes.", type=int)
    parser.add_argument('-d', '--data', nargs='+',type=lambda x: int(x,0), help="Data to write to ultra expander.")
    actions.add_argument("-w", "--write", action='store_true', help="Write to ultra expander")
    actions.add_argument("-r", "--read", action='store_true', help="Read from ultra expander")
    args = parser.parse_args()

    p = args.port
    s = 115200
    port = serial.Serial(p, s, timeout=1)
    data = []

    read_addr  = args.device << 1 | 1
    write_addr =  args.device << 1

    # enter PirateBus in I2C mode
    enter_in_i2c_mode(port)


    if args.write:
        print "Write to ultra expander..."
        address = args.device << 1
        adr2 = ((args.register >> 8) & 0xFF) 
        adr1 = ((args.register) & 0xFF) 

        for i in range(0,1):
            data = []
            data.append(write_addr)
            data.append(adr1)
            data.append(adr2)
            data.extend(args.data[0:4])
            #data.extend([i])
            #data.extend([0, 64, 0, 10])

            bytestring =  ''.join(map(chr, data))
            frame = ' '.join('0x{:02x}'.format(x) for x in data)

            crc8 = crcmod.predefined.mkCrcFun('crc-8')
            crc = crc8(bytestring, 0x00)
            crc = crc & 0xFF

            crc_str = '0x{:02x}'.format(crc)
            frame_str = "[{} {}]\n".format(frame, crc_str)

            print "Frame to send: {:s}".format(frame_str)
            port.write(frame_str)
            time.sleep(0.04)

    elif args.read:
        print "Read from ultra expander..."


        
        adr2 = ((args.register >> 8) & 0xFF) 
        adr1 = ((args.register) & 0xFF) 
        for i in range(0,1):
            data = []
            data.append(write_addr)
            data.append(adr1)
            data.append(adr2)

            bytestring =  ''.join(map(chr, data))
            frame = ' '.join('0x{:02x}'.format(x) for x in data)

            print frame

            crc8 = crcmod.predefined.mkCrcFun('crc-8')
            crc = crc8(bytestring, 0x00)
            crc = crc & 0xFF

            crc_str = '0x{:02x}'.format(crc)
            frame_str = "[{} {}[{} r:{}]\n".format(frame, hex(crc), hex(read_addr), args.bytes + 1)

            port.write("[{} {}]\n".format(frame, hex(crc)))
            time.sleep(0.1)
            port.write("[{}  r:{}]\n".format(hex(read_addr), args.bytes + 1))
            time.sleep(0.1)
            print port.read(1000)



    # print data


    #data = [0x1E, 0x02, 0x0c, 0x00]
    # data_to_read  = [0x1F, 0x10, 0x02]





    port.close()

        
