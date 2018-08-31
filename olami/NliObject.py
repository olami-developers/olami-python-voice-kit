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

from DialogueObject import DialogueObject
from StockSemantic import StockSemantic
from RestaurantSemantic import RestaurantSemantic

class NliObject(object):
    '''
    classdocs
    '''
    
    semanticMap = { \
        "stock":StockSemantic, \
        "restaurant": RestaurantSemantic, \
        }

    def __init__(self, params):
        '''
        Constructor
        '''       
        if params != None and len(params) > 0:
            self.obj = params[0]
        else:
            self.boj = None
     
    def parse(self):
        ret = None
        if self.obj != None:
            self.desc_obj = self.obj.get("desc_obj")
            if self.desc_obj != None:
                status = self.desc_obj.get("status", 1)
                if status == 0:
                    ret = True
            self.type = self.obj.get("type")
            self.dataObjs = self.obj.get("data_obj")
            self.semanticObjs = self.obj.get("semantic")
            
            if self.desc_obj != None:
                ret = DialogueObject(self.type, self.desc_obj, self.dataObjs)
            elif self.semanticObjs != None:
                classType = NliObject.semanticMap.get(self.type, None)
                if classType != None:
                    ret = classType(self.type, self.desc_obj, self.semanticObjs)
            else:
                ret = DialogueObject(self.type, self.desc_obj, self.dataObjs)           
        return ret
