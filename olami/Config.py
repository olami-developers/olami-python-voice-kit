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

class Config(object):
    '''
    classdocs
    '''
    
    '''
    - Use the server "cn.olami.ai" for China, for example:
    NLI_SERVER = "https://cn.olami.ai/cloudservice/api"
    - Use the server "tw.olami.ai" for Taiwan, for example: 
    NLI_SERVER = "https://tw.olami.ai/cloudservice/api"
    '''
    NLI_SERVER = "https://tw.olami.ai/cloudservice/api"
    APP_KEY = "*******your app key*******"
    APP_SECRET = "*******your app secret*******"

    def __init__(self, params):
        '''
        Constructor
        '''
        
