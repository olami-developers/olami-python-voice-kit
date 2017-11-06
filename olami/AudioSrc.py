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
import wave
from pyaudio import PyAudio,paInt16
from threading import Thread, RLock
import time

class AudioSrc(Thread):
    '''
    classdocs
    '''   
    RECORD_DATA_LEN = 160 * 6
    RECORD_DATA_MAX_COUNT = 700
    RECORD_DATA_MAX_HIS = 200
        
    def __init__(self):
        self.needStop = False
        self.data = []
        self.curPos = 0
        self.lock = RLock()
        Thread.__init__(self, name = "AudioSrc")
        
    def save_wave_file(self, filename, data):
        '''save the date to the wavfile'''
        wf=wave.open(filename,'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(data))
        wf.close()

        
    def limitBufLen(self):
        with self.lock:
            if len(self.data) >= AudioSrc.RECORD_DATA_MAX_COUNT:
                self.curPos = len(self.data) - AudioSrc.RECORD_DATA_MAX_COUNT // 2
                
            if self.curPos >= AudioSrc.RECORD_DATA_MAX_HIS * 2:
                removeCount = self.curPos - AudioSrc.RECORD_DATA_MAX_HIS
                del self.data[0:removeCount]
                self.curPos -= removeCount
        


    def clearData(self):
        with self.lock:
            self.data = []
            self.curPos = 0



    def getRecordData(self):
        ret = None
        waitTime = 0
        
        #print("getRecordDatalen")
        while ret == None and waitTime < 100:
            with self.lock:
                if len(self.data) > self.curPos:
                    ret = self.data[self.curPos]
                    self.curPos += 1

            if ret == None:
                waitTime += 1
                time.sleep(0.001)

        return ret
    
    def getRecordDataEx(self, maxBlock):
        ret = None
        waitTime = 0
        
        #print("getRecordDatalen")
        while ret == None and waitTime < 100:
            with self.lock:
                if len(self.data) > self.curPos:
                    if maxBlock > len(self.data) - self.curPos:
                        maxBlock = len(self.data) - self.curPos
                    ret = self.data[self.curPos:self.curPos + maxBlock]
                    self.curPos += maxBlock
                    self.limitBufLen()

            if ret == None:
                waitTime += 1
                time.sleep(0.001)

        return ret
    
    def getRecordDataAll(self):
        ret = None
        waitTime = 0
        
        #print("getRecordDatalen")
        while ret == None and waitTime < 100:
            with self.lock:
                if len(self.data) > self.curPos:
                    ret = self.data[self.curPos:]
                    self.curPos = len(self.data)
                    self.limitBufLen()

            if ret == None:
                waitTime += 1
                time.sleep(0.001)

        return ret


    def getCurRecordList(self):
        ret = None
        with self.lock:
            if len(self.data) > self.curPos:
                ret = self.data[self.curPos:]
                self.curPos = len(self.data)
                self.limitBufLen()

        return ret


    def getLastConsumedData(self, samples):
        ret = None
        count = samples // AudioSrc.RECORD_DATA_LEN
        with self.lock:
            pos = self.curPos - count
            if pos >= 0 and pos < self.curPos:
                ret = self.data[pos, self.curPos]
        return ret


    def restoreData(self, samples):
        count = (samples + AudioSrc.RECORD_DATA_LEN - 1) // AudioSrc.RECORD_DATA_LEN

        with self.lock:
            if self.curPos >= count:
                self.curPos -= count



    def getBufferDataLen(self):
        length = 0
        with self.lock:
            length = (len(self.data) - self.curPos) * AudioSrc.RECORD_DATA_LEN

        return length
    
    def startRecord(self):   
        self.needStop = False
        self.setDaemon(True)
        self.start()
        
        
    def stopRecord(self):
        self.needStop = True
        self.join(2000)
    
    def run(self):
        try:
            pa = PyAudio()  
            stream = pa.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=AudioSrc.RECORD_DATA_LEN)  
            while not self.needStop:  
                string_audio_data = stream.read(AudioSrc.RECORD_DATA_LEN)
                with self.lock:
                    self.data.append(string_audio_data)
                    
                self.limitBufLen()
                #add sleep for avoid high cpu usage
                time.sleep(0.001)
            
            #    print(len(self.data))         
            
            pa.close(stream)
        except:
            print("AudioSrc is destroyed")
       
            
            
