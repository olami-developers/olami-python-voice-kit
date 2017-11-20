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
from ctypes import CDLL,c_char_p,c_float
from threading import Thread
import os
from LedControl import LedControl

class PlayThread(Thread):
        def __init__(self, player, speech):
            self.player = player
            self.speech = speech
            Thread.__init__(self, name = "PlayThread")
        
        def run(self):
            c_speech = c_char_p(self.speech.encode('utf-8'))
            self.player.ttsLib.ttsSpeak(self.player.tts, c_speech)
            if not self.player.needStop:
                if self.player.onPlayEnd != None:
                    self.player.onPlayEnd(self.player.onPlayEndParam)            
            

class TtsPlayer(object):
    '''
    classdocs
    '''

    def __init__(self):
        #self.ttsLib = CDLL('./libs/libTtsPulseAudio.so')
        self.ttsLib = CDLL('./libs/libTts.so')
        
    def init(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        res = dir_path + '/res/tts_res.mp3'
        c_res = c_char_p(res.encode('utf-8'))
        self.tts = self.ttsLib.ttsCreate(c_res) 
        self.needStop = False  
        self.onPlayEnd = None
        self.playThread = None
        if self.tts != None:
            self.ttsLib.ttsSetSpeed(self.tts, c_float(1.1))
            return True
        else:
            return False
            
        
        
    def destroy(self):
        self.stop()
        self.ttsLib.ttsDestory(self.tts)

    
    def speak(self, speech, onPlayEnd = None, onPlayEndParam = None):
        ledctrl = LedControl()
        ledctrl.LightAll("blue")
        self.needStop = False
        self.onPlayEnd = onPlayEnd
        self.onPlayEndParam = onPlayEndParam
        self.playThread = PlayThread(self, speech)
        self.playThread.setDaemon(True)
        self.playThread.start()
        
    def stop(self):
        self.needStop = True
        self.ttsLib.ttsStop(self.tts)
        
        if self.playThread != None:
            self.playThread.join(2000)
            self.playThread = None
        
        
        
    
