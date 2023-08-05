'Aldebaran Data API Client (python)'

import re
import json
import six
import tempfile
import os
from datetime import datetime
from sys import version_info

from Aldebaran.util import getParentAndBase
from Aldebaran.data import DataObject, DataObjectType
from Aldebaran.errors import DataApiError

try:
    from urllib.parse import urlparse
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlparse
    from urllib import urlencode

class DataFile(DataObject):
    def __init__(self, client, dataUrl):
        super(DataFile, self).__init__(DataObjectType.file)
        self.client = client
        self.path = re.sub(r'^data://|^/', '', dataUrl)
        self.url = '/v1/data/' + self.path
        self.last_modified = None
        self.size = None
        self.filename = os.path.basename(self.url)
        self.presign_url = '/v1/presign'

    def set_attributes(self, attributes):
        self.last_modified = datetime.strptime(attributes['last_modified'],'%Y-%m-%dT%H:%M:%S.000+09:00')
        self.size = attributes['size']

    def get(self):
        json = self.client.getHelper(self.url).json()
        return self.client.getS3Helper(json['url'])

    def getFile(self):
        exists, error = self.existsWithError()
        if not exists:
            raise DataApiError('unable to get file {} - {}'.format(self.path, error))
        response = self.get()
        with tempfile.NamedTemporaryFile(delete = False) as f:
            for block in response.iter_content(1024):
                if not block:
                    break
                f.write(block)
            f.flush()
            return open(f.name)

    def getName(self):
        _, name = getParentAndBase(self.path)
        return name

    def getBytes(self):
        exists, error = self.existsWithError()
        if not exists:
            raise DataApiError('unable to get file {} - {}'.format(self.path, error))
        return self.get().content

    def getString(self):
        exists, error = self.existsWithError()
        if not exists:
            raise DataApiError('unable to get file {} - {}'.format(self.path, error))
        return self.get().text

    def getJson(self):
        exists, error = self.existsWithError()
        if not exists:
            raise DataApiError('unable to get file {} - {}'.format(self.path, error))
        return self.get().json()

    def exists(self):
        exists, error = self.existsWithError()
        return exists

    def existsWithError(self):
        response = self.client.headHelper(self.url)
        error = None
        if 'X-Error-Message' in response.headers:
            error = response.headers['X-Error-Message']
        return (response.status_code == 200, error)

    def put(self, data):
        s3_info = self.presign()
        id = os.path.basename(urlparse(s3_info['url']).path)

        if 'BufferedReader' != data.__class__.__name__:
            if isinstance(data, six.string_types) and not isinstance(data, six.binary_type):
                data = bytes(data.encode())

            if not isinstance(data, six.binary_type):
                raise TypeError("Must put strings or binary data. Use putJson instead")
            
        result = self.client.putS3Helper(s3_info['url'], data, s3_info['headers'])
        if result.status_code != 200:
            raise DataApiError('S3 request is status_code:{}'.format(result.status_code))
            
        data = {
            "id": id,
            "storage": 'cache',
            "metadata": {
                "size":      0,
                "filename":  self.filename
            }
        }
        
        result = self.client.putHelper(self.url, json.dumps(data))
        if 'error' in result:
            raise DataApiError(result['error']['message'] if 'message' in result['error'] else result['error'])
        else:
            return result['filepath']

    def putJson(self, data):
        return self.put(json.dumps(data))

    def putFile(self, path):
        with open(path, 'rb') as f:
            return self.put(f)

    def delete(self):
        result = self.client.deleteHelper(self.url)
        if 'error' in result:
            raise DataApiError(result['error']['message'] if 'message' in result['error'] else result['error'])
        else:
            return True

    def presign(self):
        return self.client.getHelper(self.presign_url).json()
