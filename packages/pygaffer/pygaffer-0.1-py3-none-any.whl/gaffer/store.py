from gaffer import *
import os
import requests
import json

class Gaffer:

    def __init__(self, url=None):
        if url == None:
            url = os.getenv("GAFFER")
        if url == None:
            url = "https://localhost:8080"
        self.url = url
        self.session = requests.Session()

    def use_cert(self, key=None, cert=None, ca=None, private=None):
        if private == None:
            private = os.getenv("PRIVATE")
        if private == None:
            private = os.getenv("HOME") + "/private"
        if key == None:
            key = private + "/key.me"
        if cert == None:
            cert = private + "/cert.me"
        if ca == None:
            ca = private + "/cert.ca"

        self.session.cert = (cert, key)
        self.session.verify = (ca)

    def get_all(self, entities=[], edges=[]):
        return GetAllElements(entities, edges)

    def limit(self, lim):
        return Limit(lim)

    def operation_chain(self, lst):
        return OperationChain(lst)

    def execute(self, ops):

        if type(ops) == dict:
            data = json.dumps(ops)
        else:
            data=json.dumps(ops.encode())
                            
        url = self.url + "/rest/v2/graph/operations/execute"

        headers = { "Content-Type": "application/json" }
        res = self.session.post(url, data, headers=headers)

        if res.status_code != 200:
            raise GafferError("Status %d: %s" % (res.status_code, res.text))
        
        return res.json()

    def execute_chunked(self, ops):

        if type(ops) == dict:
            data = json.dumps(ops)
        else:
            data=json.dumps(ops.encode())

        url = self.url + "/rest/v2/graph/operations/execute/chunked"

        headers = { "Content-Type": "application/json" }

        res = self.session.post(url, data, headers=headers, stream=True)

        if res.status_code != 200:
            raise GafferError("Status %d: %s" % (res.status_code, res.text))

        return res.iter_lines()

    def post(self, path, data=None, stream=False):
        
        headers = { "Content-Type": "application/json" }
        url = self.url + path
  
        res = self.session.post(url,
                                data=data,
                                headers=headers,
                                stream=stream)

        if res.status_code != 200:
            raise GafferError("Status %d: %s" % (res.status_code, res.text))
        
        return res

    def get(self, path, stream=False):
        
        headers = { "Content-Type": "application/json" }
        url = self.url + path
  
        res = self.session.get(url, stream=stream)

        if res.status_code != 200:
            raise GafferError("Status %d: %s" % (res.status_code, res.text))
        
        return res

