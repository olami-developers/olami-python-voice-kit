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
from threading import Thread
from MsgHandler import MsgHandler, MsgConst
from TtsPlayer import TtsPlayer
from SpeechProcess import SpeechProcess
from NliObject import NliObject
from LedControl import LedControl
from DialogueObject import DialogueObject

class ControlCenter(Thread):
    '''
    classdocs
    '''    
    def onServerTtsEndListener(self, param):
        if param != None:
            msg = self.handler.obtainMessage1(MsgConst.MSG_SERVER_TTS_END)
            msg.arg1 = param
            self.handler.sendMessage(msg);

    
    def onTtsEndListener(self, param):
        msg = self.handler.obtainMessage1(MsgConst.MSG_NORMAL_TTS_END)
        msg.arg1 = param
        self.handler.sendMessage(msg);
    
    def onServerTtsPlay(self, msg):
        self.ttsPlayer.stop()
        self.ttsPlayer.speak(msg.obj, self.onServerTtsEndListener, msg.arg1 != 0)
    
    def onServerTtsEnd(self, msg):
        if msg.arg1:
            self.speechProcess.wakeupNow()

    def onTtsPlay(self, msg):
        self.ttsPlayer.stop()
        self.ttsPlayer.speak(msg.obj, self.onTtsEndListener)
    
    def onTtsEnd(self, msg):
        pass
    
    def onMusicStart(self, msg):
        pass
    
    def onMusicEnd(self, msg):
        pass

    def onAdjustVol(self, msg):
        pass
    
    def onServerSessionBroken(self, msg):
        pass
    
    def onDataFromServer(self, msg):
        #obj = SemanticObject(msg.obj)
        obj = NliObject(msg.obj)
        obj = obj.parse()
	
        if type(obj) != DialogueObject:
            print("No Answer!")
            msg = self.handler.obtainMessage1(MsgConst.MSG_SERVER_TTS_PLAY)
            msg.obj = "沒有結果"
            self.handler.sendMessage(msg)
        else:
            obj.process(self.handler)
            if len(obj.getTts()) > 0:
                msg = self.handler.obtainMessage1(MsgConst.MSG_SERVER_TTS_PLAY)
                msg.obj = obj.getTts()
                msg.arg1 = obj.needAnswer()
                self.handler.sendMessage(msg)             
    
    def onUserDataRefresh(self, msg):
        pass

    def OnProcessServerQuerySuccessed(self, msg):
        pass
    
    def onMusicPlay(self, msg):
        pass
    
    def onMusicControl(self, msg):
        pass
    
    def onMusicStop(self, msg):
        pass

    def onMusicStopAudioBook(self, msg):
        pass
    
    def onForceStopTts(self, msg):
        self.ttsPlayer.stop()
    
    def __init__(self):        
        self.mExit = False
        self.msgMap = {\
            MsgConst.MSG_SERVER_TTS_PLAY : self.onServerTtsPlay, \
            MsgConst.MSG_SERVER_TTS_END : self.onServerTtsEnd, \
            MsgConst.MSG_NORMAL_TTS_PLAY : self.onTtsPlay, \
            MsgConst.MSG_NORMAL_TTS_END : self.onTtsEnd, \
            MsgConst.MSG_MUSIC_START : self.onMusicStart, \
            MsgConst.MSG_MUSIC_END : self.onMusicEnd, \
            MsgConst.MSG_ADJUST_VOL : self.onAdjustVol, \
            MsgConst.MSG_SERVER_SESSION_BROKEN : self.onServerSessionBroken, \
            MsgConst.MSG_DATA_FROM_SERVER : self.onDataFromServer, \
            MsgConst.MSG_USER_DATA_REFRESH : self.onUserDataRefresh, \
            MsgConst.MSG_PROCESS_SERVER_QUERY_SUCCESSED : self.OnProcessServerQuerySuccessed, \
            MsgConst.MSG_MUSIC_PLAY : self.onMusicPlay, \
            MsgConst.MSG_MUSIC_CONTROL : self.onMusicControl, \
            MsgConst.MSG_MUSIC_STOP : self.onMusicStop, \
            MsgConst.MSG_STOP_AUDIOBOOK : self.onMusicStopAudioBook, \
            MsgConst.MSG_FORCE_STOP_TTS : self.onForceStopTts, \
        }
        Thread.__init__(self, name = "ControlCenter")
        
    def handleMessage(self, msg):        
        if msg.what in self.msgMap.keys():
            self.msgMap[msg.what](msg)
        
    
    
    def init(self):        
        self.handler = MsgHandler()
        self.ttsPlayer = TtsPlayer()
        self.speechProcess = SpeechProcess()
        ret = self.ttsPlayer.init()
        if ret:
            self.ttsPlayer.speak("你好，我是歐拉蜜", None)
            ret = self.speechProcess.init(self.handler)
           
        return ret
        
    def run(self):
        while not self.mExit:
            msg = self.handler.msgQueue.getNext()
            print("processing message %d" % (msg.what))
            if msg.what == MsgConst.MSG_SERVER_TTS_END:
                ledctrl = LedControl()
                ledctrl.LightAll("green")
            if msg != None:
                self.handleMessage(msg)                 

    def uninit(self):
        if self.ttsPlayer:
            self.ttsPlayer.destroy()
        
        if self.ttsPlayer:
            self.ttsPlayer.destroy()
