'''MIT License

Copyright (c) 2019 {Zero Cool} & Aditya Nugraha Kalimantan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

# -*- coding: utf-8 -*-
from . import Utils,to_json,dumps,OrderedDict,DevLTypes
import json
from .photofunia import path
from collections import namedtuple

class PhotoFunia(DevLTypes):
    def __init__(self,dict):
        vars(self).update(dict)

    def __repr__(self):
        return self.default()

class Config(Utils):

    def __init__(self):
        super(Config, self).__init__()
        self.path = PhotoFunia(path)
        self.params = {
        	'access_key': 'e3084acf282e8323181caa61fa305b2a',
        	'lang': 'en'
        }
        self.bool_dict = {
        	True: ['yes', 'active'],
        	False: ['no', 'deactive']
        }

    def response(self,url=None,data=None,files=None):
        if url:
            data = self.postContent(url, data=data,files=files)
        return PhotoFunia(data.json())