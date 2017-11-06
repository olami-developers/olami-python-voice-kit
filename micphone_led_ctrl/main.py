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

Created on 2017年7月18日

@author: JeffHuang
'''
from uartapi import UartAPISample
import time

def print_menu():       ## Your menu design here
    print (30 *"-" , "MENU" , 30 * "-")
    print ("0. exit")
    print ("1. RED")
    print ("2. BLUE")
    print ("3. GREEN")
    print ("4. WHITE")
    print ("5. DARK")
    print ("6. ROTATE")
    print ("7. FADE")
    print ("8. ACKNAK")
    print ("9. button(get button press)")
    print (67 * "-")
  
      

def main():
    print("\n----- Test UART API-----\n")
    
    uartApi = UartAPISample()
    
    uartApi.openUart()

    if uartApi.uartIsOpen():

        try:
            '''flush input buffer, discarding all its contents'''
            uartApi.ser.flushInput()
            '''flush output buffer, aborting current output 
               and discard all that is in buffer'''
            uartApi.ser.flushOutput()#
 
            loop=True
            while loop:          ## While loop which will keep going until loop = False
                print_menu()    ## Displays menu
                choice = input("Enter your choice [0-9]: ")
     
                if choice==0:
                    loop=False
                elif choice==1:     
                    uartApi.RunRED()
                elif choice==2:
                    uartApi.RunBLUE()
                elif choice==3:
                    uartApi.RunGREEN()
                elif choice==4:
                    uartApi.RunWHITE()
                elif choice==5:
                    uartApi.RunDARK()
                elif choice==6:
                    uartApi.RunROTATE()
                elif choice==7:
                    uartApi.RunFADE()
                elif choice==8:
                    uartApi.RunACKNAK()
                elif choice==9:
                    numOfLines = 0
                    while True:
                        response = uartApi.ser.readline()
                        print("read data: " + response)
                        numOfLines = numOfLines + 1
                        if (numOfLines >= 30):
                            break
                else:
                    input("Wrong option selection. Enter any key to try again..")
            uartApi.closeUart()
        except Exception as e1:
            print ("error communicating...: " + str(e1))

    else:
        print ("cannot open serial port ")

    
if __name__ == '__main__':
    main()