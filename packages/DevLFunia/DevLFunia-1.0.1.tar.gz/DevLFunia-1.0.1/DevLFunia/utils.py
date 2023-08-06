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
from . import requests,DevLTypes,base64,urllib

class Utils(DevLTypes):

    def __init__(self):
        super(Utils, self).__init__()
        self._session = requests.Session()
        self.host = 'https://api.photofunia.com/2.0/effects/'

    def urlEncode(self, url, path, params=[]):
        try:    # Works with python 2.x
            return url + path + '?' + urllib.urlencode(params)
        except: # Works with python 3.x
            return url + path + '?' + urllib.parse.urlencode(params)

    def optionsContent(self, url, data=None, headers=None):
        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        return self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        return self._session.put(url, headers=headers, data=data)

    def __repr__(self):
        return self.default()