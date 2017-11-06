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
from AudioSrc import AudioSrc
from MsgHandler import MsgConst
from OlamiNlp import OlamiNlp
from VoiceCmd import VoiceCmd
from threading import Thread
from Config import Config
import time
class SpeechProcess(Thread):
    '''
    classdocs
    '''
    def __init__(self):
        Thread.__init__(self, name = "SpeechProcess")
        
        
    def init(self, handler):
        self.handler = handler  
        self.audioSrc = AudioSrc()        
        self.audioSrc.startRecord()  
        self.voiceCmd = VoiceCmd()
        self.voiceCmd.init(self.audioSrc)
        self.setDaemon(True)
        self.nlp = OlamiNlp()
        self.nlp.setLocalization(Config.NLI_SERVER)
        self.nlp.setAuthorization(Config.APP_KEY, Config.APP_SECRET)     
        self.start()      
        return True
    
    def destroy(self):
        self.needStop = True
        self.join(2000)        
        self.audioSrc.stopRecord()        
        self.voiceCmd.destroy()
        
    def wakeupNow(self):
        self.voiceCmd.cancelDetect()

    def run(self):
        self.needStop = False        
        
        while not self.needStop:
            wakeup = self.voiceCmd.startDetect()
            self.handler.sendEmptyMessage(MsgConst.MSG_FORCE_STOP_TTS)
            if wakeup != VoiceCmd.STATE_STOPPED:  
                    
                if wakeup == VoiceCmd.STATE_DETECTED_KEY:
                    msg = self.handler.obtainMessage1(MsgConst.MSG_NORMAL_TTS_PLAY)
                    msg.obj = "在"                
                    self.handler.sendMessage(msg)
                    time.sleep(0.5)
                    self.audioSrc.clearData() 
                nlpResult = self.nlp.getNlpResult(self.audioSrc)
                if nlpResult != None:
                    msg = self.handler.obtainMessage1(MsgConst.MSG_DATA_FROM_SERVER)
                    msg.obj = nlpResult            
                    self.handler.sendMessage(msg)
                
                self.audioSrc.clearData()
                
                
        
        
        
        