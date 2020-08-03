"""
    rms-watchdog - Power management and watchdog board for Winlink gateway
    Copyright 2018, 2019 by Michael R. McPherson, Charlottesville, VA
    mailto:mcpherson@acm.org
    http://www.kq9p.us

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
 
__author__ = 'Michael R. McPherson <mcpherson@acm.org>'

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import adafruit_ina260

def numbers_to_keys(keyCode):
    switcher = {
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "0",
        11: "*",
        12: "#",
        13: "A",
        14: "B",
        15: "C",
        0: "D"
    }
    return switcher.get(keyCode, "invalid keycode")


def main():
    stq = DigitalInOut(board.D2)
    stq.direction = Direction.INPUT
    q1 = DigitalInOut(board.D3)
    q1.direction = Direction.INPUT
    q2 = DigitalInOut(board.D4)
    q2.direction = Direction.INPUT
    q3 = DigitalInOut(board.D5)
    q3.direction = Direction.INPUT
    q4 = DigitalInOut(board.D6)
    q4.direction = Direction.INPUT

    i2cbus = busio.I2C(board.SCL, board.SDA)
    ina260v12 = adafruit_ina260.INA260(i2cbus, 0x40)
    # ina260v5 = adafruit_ina260.INA260(i2cbus, 0x41)

    uart = busio.UART(board.TX, board.RX, baudrate=1200)

    decoderLocked = False
    newKeyCode = 0

    while(True):
        if(stq.value):
            if(not decoderLocked):
                newKeyCode = (q1.value) + (q2.value * 2) + (q3.value * 4) + (q4.value * 8)
                decoderLocked = True
                print("keyCode", numbers_to_keys(newKeyCode))
                print("Current:", ina260v12.current)
                print("Voltage:", ina260v12.voltage)
                print("Power:", ina260v12.power)
        else:
            decoderLocked = False
        uart.write(bytearray(b'ping'))
        data = uart.readline()
        print(data)
        time.sleep(1.0)
        


if __name__ == "__main__":
    # execute only if run as a script
    main()
