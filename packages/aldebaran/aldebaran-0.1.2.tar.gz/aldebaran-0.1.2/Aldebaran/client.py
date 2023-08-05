'Aldebaran API Client (python)'

import Aldebaran
from Aldebaran.algorithm import Algorithm
from Aldebaran.datafile import DataFile
from Aldebaran.datadirectory import DataDirectory

import json, re, requests, six
import os

class Client(object):
    'Aldebaran Common Library'

    apiKey = None
    apiAddress = None

    def __init__(self, apiKey = None, apiAddress = None):
        if apiKey is None and 'ALDEBARAN_API_KEY' in os.environ:
            apiKey = os.environ['ALDEBARAN_API_KEY']
        self.apiKey = apiKey
        if apiAddress is not None:
            self.apiAddress = apiAddress
        else:
            self.apiAddress = Aldebaran.getApiAddress()

    def algo(self, algoRef):
        return Algorithm(self, algoRef)

    def file(self, dataUrl):
        return DataFile(self, dataUrl)

    def dir(self, dataUrl):
        return DataDirectory(self, dataUrl)

    def postJsonHelper(self, url, input_object, parse_response_as_json=True, content_type=None, **query_parameters):
        headers = {}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey

        input_json = None
        if input_object is None:
            input_json = json.dumps(None).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        elif isinstance(input_object, six.string_types):
            input_json = input_object.encode('utf-8')
            headers['Content-Type'] = 'text/plain'
        elif isinstance(input_object, bytearray) or isinstance(input_object, bytes):
            input_json = bytes(input_object)
            headers['Content-Type'] = 'application/octet-stream'
        else:
            input_json = json.dumps(input_object).encode('utf-8')
            headers['Content-Type'] = 'application/json'
        if content_type is not None:
            headers['Content-Type'] = content_type

        response = requests.post(self.apiAddress + url, data=input_json, headers=headers, params=query_parameters)

        if parse_response_as_json:
            return response.json()
        return response

    def getHelper(self, url, **query_parameters):
        headers = {}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey
        return requests.get(self.apiAddress + url, headers=headers, params=query_parameters)

    def patchHelper(self, url, params):
        headers = {'content-type': 'application/json'}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey
        return requests.patch(self.apiAddress + url, headers=headers, data=json.dumps(params))

    def headHelper(self, url):
        headers = {}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey
        return requests.head(self.apiAddress + url, headers=headers)

    def putHelper(self, url, data):
        headers = {}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey
        response = requests.put(self.apiAddress + url, data=data, headers=headers)
        return response.json()

    def deleteHelper(self, url):
        headers = {}
        if self.apiKey is not None:
            headers['Authorization'] = "Token " + self.apiKey
        response = requests.delete(self.apiAddress + url, headers=headers)
        return response.json()

    def putS3Helper(self, url, data, headers = {}):
        response = requests.put(url, data=data, headers=headers)
        return response

    def getS3Helper(self, url, headers = {}):
        response = requests.get(url, headers=headers)
        return response
