'Aldebaran API Client (python)'

from Aldebaran.client import Client
import os

apiKey = None
apiAddress = None

def algo(algoRef):
    return getDefaultClient().algo(algoRef)

def file(dataUrl):
    return getDefaultClient().file(dataUrl)

def dir(dataUrl):
    return getDefaultClient().dir(dataUrl)

def client(api_key=None, api_address=None):
    return Client(api_key, api_address)

defaultClient = None

def getDefaultClient():
    global defaultClient
    if defaultClient is None or defaultClient.apiKey is not apiKey:
        defaultClient = Client(apiKey)
    return defaultClient

def getApiAddress():
    global apiAddress
    if apiAddress is not None:
        return apiAddress
    elif 'ALDEBARAN_API' in os.environ:
        return os.environ['ALDEBARAN_API']
    else:
        return 'https://aldebaran.signate.jp/api'
