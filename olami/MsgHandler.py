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

from threading import Condition
import time

class Message(object):
    def __init__(self):
        self.what = 0
        self.arg1 = 0
        self.arg2 = 0
        self.obj = 0    
        self.when = 0


class MsgConst(object):

    MSG_SERVER_TTS_PLAY = 1
    MSG_SERVER_TTS_END = 2
    MSG_NORMAL_TTS_PLAY = 3
    MSG_NORMAL_TTS_END = 4
    MSG_MUSIC_START = 5
    MSG_MUSIC_END = 6
    MSG_ADJUST_VOL = 7
    MSG_SERVER_SESSION_BROKEN = 8
    MSG_DATA_FROM_SERVER = 9
    MSG_USER_DATA_REFRESH = 10
    MSG_PROCESS_SERVER_QUERY_SUCCESSED = 11
    MSG_MUSIC_PLAY = 12
    MSG_MUSIC_CONTROL = 13
    MSG_MUSIC_STOP = 14
    MSG_STOP_AUDIOBOOK = 15
    MSG_FORCE_STOP_TTS = 16    
    
    def __init__(self):
        pass


class MessageQueue(object):
    def __init__(self):
        self.mLstMsg = []
        self.con = Condition()
        self.block = True
        
    def insertMessage(self, msg, when): 
        ret = False
        #print("insertMessage 111: %d %f" % (msg.what, msg.when))
        with self.con:
            pos = len(self.mLstMsg)
            i = 0;
            while i < pos:            
                if self.mLstMsg[i].when > when:
                    pos = i;
                    break; 
                i += 1               
                    
            msg.when = when      
            self.mLstMsg.insert(pos, msg)
            self.con.notify()
            ret = True
        return ret

    
    def removeMessage(self, what):
        with self.con:
            i = len(self.mLstMsg) - 1
            while i >= 0:
                if self.mLstMsg[i].what == what:
                    del self.mLstMsg[i]
                i -= 1
            self.con.notify()

    def getNext(self):
        ret = None
        delta = -1;
        while self.block:
            with self.con:
                if len(self.mLstMsg) > 0:
                    ret = self.mLstMsg[0]
                    delta = ret.when - time.time();
                    if delta <= 0:
                        ret = self.mLstMsg[0]
                        del self.mLstMsg[0]
                        break;
                    else:
                        ret = None

                if delta > 0:
                    self.con.wait(delta)
                else:
                    self.con.wait()
        return ret;        

    
    def needBlock(self, block):
        with self.con:
            self.block = block
            self.con.notify()

    def quit(self):
        with self.con:
            self.block = False
            self.con.notify()


class MsgHandler(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.msgQueue = MessageQueue()
        
        
    def sendMessage(self, msg):
        return self.sendMessageDelayed(msg, 0)

    def sendEmptyMessage(self, what):
        return self.sendEmptyMessageDelayed(what, 0);


    def sendEmptyMessageDelayed(self, what, delayMillis):
        msg = Message()
        msg.what = what
        return self.sendMessageDelayed(msg, delayMillis)

    def sendMessageDelayed(self, msg, delayMillis):
        if delayMillis < 0:
            delayMillis = 0
        return self.sendMessageAtTime(msg, time.time() + delayMillis / 1000.0);

    
    def sendEmptyMessageAtTime(self, what, uptimeMillis):
        msg = Message()
        msg.what = what;
        return self.sendMessageAtTime(msg, uptimeMillis)

    def sendMessageAtTime(self, msg, uptimeMillis):        
        return self.msgQueue.insertMessage(msg, uptimeMillis);
    
    
    def obtainMessage(self):
        return Message()


    def obtainMessage1(self, what):
        msg = Message()
        msg.what = what
        return msg

    def obtainMessage2(self, what, obj):
        msg = Message()
        msg.what = what
        msg.obj = obj
        return msg

    def obtainMessage3(self, what, arg1, arg2):
        msg = Message()
        msg.what = what
        msg.arg1 = arg1
        msg.arg2 = arg2
        return msg


    def obtainMessage4(self, what, arg1, arg2, obj):
        msg = Message()
        msg.what = what
        msg.arg1 = arg1
        msg.arg2 = arg2
        msg.obj = obj
        return msg


    def removeMessages(self, what):
        self.msgQueue.removeMessage(what)