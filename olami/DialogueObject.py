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

class DialogueObject(object):
    '''
    classdocs
    '''

    def __init__(self, obj_type, desc_obj, data_objs):
        '''
        Constructor
        '''
        self.type = obj_type
        self.desc_obj = desc_obj
        self.dataObjs = data_objs

    def parseDataObjs(self):
        tts = None
        for dataObj in self.dataObjs:
            if self.type == "baike":
                tts = dataObj.get("description")
            elif self.type == "news":
                tts = dataObj.get("detail")
            elif self.type == "tvprogram":
                tts = dataObj.get("time")
                if tts != None:
                    tts += " "
                    tts += dataObj.get("name")
            elif self.type == "joke":
                tts = dataObj.get("content")
            elif self.type == "stock":
                tts = dataObj.get("cur_price")
            elif self.type == "cooking":
                tts = dataObj.get("content")          
            
            if tts != None:
                self.tts += tts + "。"
            
     
    def getTts(self):
        self.tts = ""
        if self.desc_obj != None:
            ttsObj = self.desc_obj.get("result")
            if ttsObj != None:
                self.tts += ttsObj
       
        if self.dataObjs != None:
            self.parseDataObjs()
            
        return self.tts
    
    def needAnswer(self):
        if self.type == "question" or self.type == "confirmation" or self.type == "selection":
            return True
        else:
            return False
        
    def process(self, handler):
        pass       