#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Copyright 2017, VIA Technologies, Inc. & OLAMI Team.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
'''
import serial, time

class UartAPISample:
    # UART Configuration Parameters
    PORT = '/dev/ttyAMA0'
    BAUD_RATE = 115200;
    DATA_BITS = serial.EIGHTBITS;
    STOP_BITS = serial.STOPBITS_ONE;
    CHUNK_SIZE = 512;
    ser = serial.Serial();
    _acknak = False;
    
    def __init__(self):
        pass
    
    def uartIsOpen(self):
        return self.ser.isOpen()
    
    def openUart(self):
        #initialization and open the port

        '''possible timeout values:
            1. None: wait forever, block call
            2. 0: non-blocking mode, return immediately
            3. x, x is bigger than 0, float allowed, timeout block call
        '''
        #check which port was realy used 確認通訊口是否ok
        print ("ser.portstr: "+ str(self.ser.portstr) +"\n")
        
        self.ser.port = self.PORT
        self.ser.baudrate = self.BAUD_RATE
        #number of bits per bytes
        self.ser.bytesize = self.DATA_BITS
        #set parity check: no parity
        self.ser.parity = serial.PARITY_NONE
        #number of stop bits 
        self.ser.stopbits = self.STOP_BITS 
        #ser.timeout = None          #block read
        self.ser.timeout = 1             #non-block read
        #ser.timeout = 2             #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 2     #timeout for write
        
        try: 
            if self.uartIsOpen() == False:
                self.ser.open()
                print("uart.open()\n")
        except Exception as e:
            print ("error open serial port: " + str(e))
            exit()
        
    def closeUart(self):
        try:
            if self.uartIsOpen():
                self.ser.close()
                print("uart.close()\n")
        except Exception as e1:
            print ("error communicating...: " + str(e1))

    
    def unsignedToBytes(self,b):
        return b & 0xFF
    
    def send_cmds(self,bff,bfsz):
        crc = 0;
        try:
            if self.uartIsOpen():
                self.ser.write(bff)
                for i in range(0, bfsz, 1):
                    crc ^= self.unsignedToBytes(bff[i])
                
                bff[0] = (crc & 0xff)
                tailbuf = bytearray()
                tailbuf.append(bff[0])
                
                self.ser.write(tailbuf)
                
        except Exception as e:
            print("Unable to transfer data over UART(2)" + str(e))
            
    _CMD_REC_SET_LED = 0x02;
    _CMD_REC_SET_SINGLE_LED = 0x03;
    _CMD_SHOW_LED = 0x04;
    _CMD_ROTATE_LED = 0x05;
    _CMD_ACKNAK = 0x06;        
    
    def fill_rgb(self, mask, maskop, r, g, b):
        bufarr = bytearray()
        bufarr.append(self._CMD_REC_SET_LED)
        bufarr.append(ord(maskop))
        bufarr.append(mask >> 8)
        bufarr.append(mask & 0xff)
        bufarr.append(r)
        bufarr.append(g)
        bufarr.append(b)
        self.send_cmds(bufarr, 7)
    
    def set_rgb(self,pos, r, g, b):
        bufarr = bytearray()
        bufarr.append(self._CMD_REC_SET_SINGLE_LED)
        bufarr.append(pos)
        bufarr.append(r)
        bufarr.append(g)
        bufarr.append(b)
        self.send_cmds(bufarr, 5)

    def show_led(self,bright): 
        bufarr = bytearray()
        bufarr.append(self._CMD_SHOW_LED)
        bufarr.append(bright)
        self.send_cmds(bufarr, 2)
    
    def rotate_led(self,dop):
        bufarr = bytearray()
        bufarr.append(self._CMD_ROTATE_LED)
        bufarr.append(ord(dop))
        self.send_cmds(bufarr, 2)

    def acknak_onoff(self,dop):
        bufarr = bytearray()
        bufarr.append(self._CMD_ACKNAK)
        bufarr.append(ord(dop))
        self.send_cmds(bufarr, 2)
        
        
    #
    def RunRED(self):
        print("Run: RED")
        self.fill_rgb(0x0fff,  'P', 255, 0, 0)
        time.sleep(10.0/1000.0)
        self.show_led(50)
    
    #GREEN
    def RunGREEN(self):
        print("Run: GREEN")
        self.fill_rgb(  0x0fff,  'P', 0, 255, 0)
        time.sleep(10.0/1000.0)
        self.show_led(50)
    
    #BLUE
    def RunBLUE(self):
        print("Run: BLUE")
        self.fill_rgb(  0x0fff,  'P',  0, 0, 255)
        time.sleep(10.0/1000.0)
        self.show_led(50)
    
    #WHITE
    def RunWHITE(self):
        print("Run: WHITE")
        self.fill_rgb(  0x0fff,  'P', 255, 255, 255)
        time.sleep(10.0/1000.0)
        self.show_led(50)
    
    #ROTATE
    def RunROTATE(self):
        print("Run: ROTATE")
        self.fill_rgb(  0x0fff,  'P', 0, 0, 0)
        time.sleep(10.0/1000.0)
        self.show_led(100)
        time.sleep(10.0/1000.0)
        self.set_rgb(  0, 0, 128, 128)

        for i in range(0,36,1):
            time.sleep(10.0/1000.0)
            self.show_led(100)
            time.sleep(10.0/1000.0)
            self.rotate_led('R')
        
        for i in range(0,36,1):
            time.sleep(10.0/1000.0)
            self.show_led(100)
            time.sleep(10.0/1000.0)
            self.rotate_led('L')
    #FADE    
    def RunFADE(self):
        print("Run: FADE")
        self.fill_rgb(  0x0fff,  'P', 0, 0, 255)
        time.sleep(10.0/1000.0)
        for i in range(0,100,10):
            time.sleep(300.0/1000.0)
            self.show_led(i)
        for i in range(100,0,-10):
            time.sleep(300.0/1000.0)
            self.show_led(i)

    #DARK 
    def RunDARK(self):
        self.fill_rgb(  0x0fff,  'P', 0, 0, 0)
        time.sleep(10.0/1000.0)
        self.show_led(0)
        
    def RunACKNAK(self):
        if self._acknak:
            self._acknak = False
            self.acknak_onoff( 'F')
        else:
            self._acknak = True
            self.acknak_onoff( 'O')
    
