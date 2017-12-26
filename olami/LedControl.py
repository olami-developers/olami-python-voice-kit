'''
	Copyright 2017, VIA Technologies, Inc. & OLAMI Team.

	http://olami.ai

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

from uartapi import UartAPISample
import time

class LedControl(object):
    '''
    classdocs
    '''
    
    enableLEDControl = 1

    def __init__(self):
        '''
        Constructor
        '''

    def LightAll(self,color):
        if self.enableLEDControl == 0:
            return
        uartApi = UartAPISample()
        time.sleep(0.001)
        uartApi.openUart()

        if uartApi.uartIsOpen():

            try:
                '''flush input buffer, discarding all its contents'''
                uartApi.ser.flushInput()
                '''flush output buffer, aborting current output 
                   and discard all that is in buffer'''
                uartApi.ser.flushOutput()

                if color == "red":
                    uartApi.RunRED()
                elif color == "blue":
                    uartApi.RunBLUE()
                elif color == "green":
                    uartApi.RunGREEN()
                elif color == "white":
                    uartApi.RunWHITE()
                else: 
                    uartApi.RunDARK()
                time.sleep(0.001)
                uartApi.closeUart()
            except Exception as e1:
                print ("error communicating...: " + str(e1))

        else:
            print ("cannot open serial port ")
     

     
