# -*- coding: utf-8 -*-
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

import time
from datetime import datetime
import hashlib
import urllib.request, urllib.error
import json
from speex import *  
from LedControl import LedControl

class OlamiNlp(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
 
    API_NAME_ASR = "asr";    

    apiBaseUrl = ''
    appKey = ''
    appSecret = ''
    cookies = ''
    

    def setAuthorization(self, appKey, appSecret):
        self.appKey = appKey
        self.appSecret = appSecret


    def setLocalization(self, apiBaseURL):
        self.apiBaseUrl = apiBaseURL
        
    def stopProcess(self):
        self.stop = True
        
    def encodeSpeex(self, audioData):
        encoder = WBEncoder()     
        encoder.quality = 10   
        vocoded = b''
        packet_size = encoder.frame_size * 2 * 1

        for i in range(0, len(audioData), packet_size):
            packet = audioData[i:i + packet_size]
            if len(packet) != packet_size:
                end = len(audioData) - len(audioData) % (encoder.frame_size * 2)
                packet = audioData[i:end]        
            raw = encoder.encode(packet)
            vocoded += raw
            
        return vocoded
    
    def encodeSpeexEx(self, audioDatas):
        encoder = WBEncoder()     
        encoder.quality = 10   
        vocoded = b''
        packet_size = encoder.frame_size * 2 * 1

        for audioData in audioDatas:
            for i in range(0, len(audioData), packet_size):
                packet = audioData[i:i + packet_size]
                if len(packet) != packet_size:
                    end = len(audioData) - len(audioData) % (encoder.frame_size * 2)
                    packet = audioData[i:end]        
                raw = encoder.encode(packet)
                vocoded += raw
            
        return vocoded
        
        
    def getNlpResult(self, audioSrc):
        ret = None
        self.cookies = None
        self.stop = False
        
        startTime = time.time()
        foundVoice = False
        ledctrl = LedControl()
        ledctrl.LightAll("white")
        print("send data~~~"+str(datetime.now()))
        speechLen = 0
        while True:
            #audioData = audioSrc.getRecordData()
            audioDatas = audioSrc.getRecordDataEx(3)  
            lenAudio = len(audioDatas) * len(audioDatas[0])            
            speexData = self.encodeSpeexEx(audioDatas)
            #print(lenAudio)
            #audioData = bytearray(audioData)
            postData = str(self.getBasicQueryString(OlamiNlp.API_NAME_ASR, "seg,nli"))
            postData += "&compress=" + "1"
            postData += "&stop=" + "0"
        
            url = str(self.apiBaseUrl) + "?" + str(postData)
            
            if self.cookies == None:
                headers = { 'Connection'    : "Keep-Alive", \
                    'Content-Type'  : "application/octet-stream" }
            else:
                headers = { 'Connection'    : "Keep-Alive", \
                    'Content-Type'  : "application/octet-stream", \
                    'Cookie': self.cookies }
                
            #print("url begin", time.time())
            req = urllib.request.Request(url,speexData, headers)
            f = urllib.request.urlopen(req)
            response = f.read().decode()
            
            #print("url return", time.time())
            #print(response + "\n")
            
            if self.cookies == None:
                self.cookies = f.getheader('Set-Cookie')
            
            resAsr = None
            speechStatus = None
            resData = None
            
            res =  json.loads(response)            
            if res != None:
                resData = res.get("data")
            
            if resData != None:
                resAsr = resData.get("asr")
                
            if resAsr != None:  
                speechStatus = resAsr.get("speech_status")
            if speechStatus == 1:
                foundVoice = True;
                speechLen += lenAudio
                
            if (not foundVoice) and time.time() > startTime + 8:
                break;
            
            
            if foundVoice and (speechStatus == 0 or speechLen > 32000 * 8):
                #final post: it need to set stop=1
                postData = str(self.getBasicQueryString(OlamiNlp.API_NAME_ASR, "seg,nli"))
                postData += "&compress=" + "1"
                postData += "&stop=" + "1"

                url = str(self.apiBaseUrl) + "?" + str(postData)
                headers = { 'Connection'    : "Keep-Alive", \
                            'Content-Type'  : "application/octet-stream", \
                            'Cookie': self.cookies }
                req = urllib.request.Request(url,speexData, headers)
                f = urllib.request.urlopen(req)
                response = f.read().decode()
                #print(response + "\n")

                startTime = time.time()
                while True:
                    response = self.getRecognitionResult(OlamiNlp.API_NAME_ASR, "nli,seg")
                    #print(response + "\n")
                    res =  json.loads(response)
                    resAsr = None
                    isFinal = None
                    resData = None
                    
                    if res != None:
                        resData = res.get("data")
                    
                    if resData != None:
                        resAsr = resData.get("asr")
                    
                        if resAsr != None:
                            isFinal = resAsr.get("final")
                            #retTemp = resAsr.get("result")     
                            #if retTemp != None:
                            #    ret = retTemp
                        
                        if isFinal:
                            ret = resData.get("nli")
                            print("get result~~~"+str(datetime.now()))
                            print(response + "\n")
                            break                                   
                    
                    if isFinal or time.time() > startTime + 10:
                        break       

                break 
        return ret
    
    '''Get the NLU recognition result for your input text.
     
      :param inputText the text you want to recognize.'''
    def getNliResult(self, inputText):
        
        '''Assemble all the HTTP parameters you want to send'''
        rq = '{\"data_type\":\"stt\",\"data\":{\"input_type\":1,\"text\":\"'+inputText+'\"}}'
        postData = str(self.getBasicQueryString("nli", ""))
        postData +='&rq='+rq
        
        '''Request NLU service by HTTP POST'''
        req = urllib.request.Request(self.apiBaseUrl,postData.encode("utf-8"))
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode('utf-8')
        
        return str(getResponse)
 
    def getRecognitionResult(self, apiName, seqValue):
        query = self.getBasicQueryString(apiName, seqValue) + "&stop=1"

        '''Request speech recognition service by HTTP GET'''
        url = str(self.apiBaseUrl) + "?" + str(query)
        req = urllib.request.Request(url,headers = {'Cookie': self.cookies})
        with urllib.request.urlopen(req) as f:
            getResponse = f.read().decode()
        
        '''Now you can check the status here.'''
        #print("Sending 'GET' request to URL : " + self.apiBaseUrl)
        #print("get parameters : " + str(query))
        #print("Response Code : " + str(f.getcode()))
        
        '''Get the response'''
        return str(getResponse)
    

    def getBasicQueryString(self, apiName, seqValue):
        timestamp = int(round(time.time() * 1000))
        
        '''Prepare message to generate an MD5 digest.'''
        signMsg = str(self.appSecret)
        signMsg += 'api='+apiName
        signMsg += 'appkey='+str(self.appKey)
        signMsg += 'timestamp='+str(timestamp)
        signMsg += str(self.appSecret)
        
        '''Generate MD5 digest.'''
        md = hashlib.md5()
        md.update(signMsg.encode('utf-8'))
        sign = md.hexdigest()
        
        '''Assemble all the HTTP parameters you want to send'''
        postData = 'appkey='+str(self.appKey)
        postData +='&api='+apiName
        postData +='&timestamp='+str(timestamp)
        postData +='&sign='+str(sign)
        postData +='&seq=' +seqValue
        postData +='&_from=python'
        
        return str(postData)

        
