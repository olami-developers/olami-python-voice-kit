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

class SemanticObject(object):
    '''
    classdocs
    '''
    def __init__(self, obj_type, desc_obj, symantic_objs):
        '''
        Constructor
        '''        
        self.type = obj_type
        self.desc_obj = desc_obj
        self.semanticObjs = symantic_objs
        self.tts = ""
            
    def getTts(self):
        return ""
    
    def process(self, handler):
        pass
    
    def needAnswer(self):
        return False

        
 
        