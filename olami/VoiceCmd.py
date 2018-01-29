#-*- coding：utf-8 -*-
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
from ctypes import CDLL,c_void_p,c_int,c_char_p,cast
from AudioSrc import AudioSrc
import os
from LedControl import LedControl

class VoiceCmd(object):
    '''
    classdocs
    '''
    STATE_CANCELED = 1              # cancel detection 
    STATE_STOPPED = 2               # stop detection
    STATE_DETECTED_KEY = 3          # just keyword is detected
    STATE_DETECTED_SENTENCE = 4     # keyword is detected and followed by other words
    
    def __init__(self):
        '''
        Constructor
        '''
    def init(self, audioSrc):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        self.openblasLib = CDLL(dir_path + '/libs/libopenblas.so')
        self.asrLib = CDLL(dir_path + '/libs/libAsrKaldi.so')
        self.audioSrc = audioSrc
        resFolder = dir_path + '/res/voicecmd'
        
        self.asrLib.voiceCmdSendAudioData.arg_types = (c_void_p, c_int, c_int)
        self.asrLib.voiceCmdSendAudioData.restype  = c_char_p
        c_resFolder = c_char_p(resFolder.encode('utf-8'))
        self.asrLib.voiceCmdInit(c_resFolder)
        
    def destroy(self):
        self.asrLib.voiceCmdUnInit()
        
    def cancelDetect(self):
        self.needCancel = True
    
    def stoplDetect(self):
        self.needStop = True
    
    def startDetect(self):
        ledctrl = LedControl()
        ledctrl.LightAll("green")
        ret = VoiceCmd.STATE_STOPPED
        self.asrLib.voiceCmdStartDetect()
        self.needStop = False
        self.needCancel = False
        
        while (not self.needStop) and (not self.needCancel):
            data = self.audioSrc.getRecordData()
            if data != None:
                pData = cast(data, c_void_p)
                hyp = self.asrLib.voiceCmdSendAudioData(pData, len(data) // 2, 0);
                if hyp:
                    hyp = hyp.decode("utf-8")
                    print(hyp)
                    if "歐拉密" == hyp:
                        if self.asrLib.voiceCmdIsSpeaking() != 0:
                            ret = VoiceCmd.STATE_DETECTED_SENTENCE                            
                        else:
                            if self.asrLib.voiceCmdGetKeyWordStart() > self.asrLib.voiceCmdGetKeyWordLen() + 16000 * 8 / 10:
                                ret = VoiceCmd.STATE_DETECTED_SENTENCE
                            else:
                                ret = VoiceCmd.STATE_DETECTED_KEY
                        
                        if ret == VoiceCmd.STATE_DETECTED_SENTENCE:
                            self.audioSrc.restoreData(self.asrLib.voiceCmdGetKeyWordStart())
                            
                        self.asrLib.voiceCmdStopDetect();
                        self.asrLib.voiceCmdStartDetect();
                        break

        if self.needStop:
            ret = VoiceCmd.STATE_STOPPED
        elif self.needCancel:
            ret = VoiceCmd.STATE_CANCELED
        return ret
    
