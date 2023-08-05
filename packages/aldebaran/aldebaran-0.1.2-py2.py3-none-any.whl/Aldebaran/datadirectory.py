'Aldebaran Data API Client (python)'

import json
import re
import six
import tempfile

import Aldebaran
from Aldebaran.datafile import DataFile
from Aldebaran.data import DataObject, DataObjectType
from Aldebaran.errors import DataApiError
from Aldebaran.util import getParentAndBase, pathJoin

class DataDirectory(DataObject):
    def __init__(self, client, dataUrl):
        super(DataDirectory, self).__init__(DataObjectType.directory)
        self.client = client
        self.path = re.sub(r'^data://|^/', '', dataUrl)
        self.url = DataDirectory._getUrl(self.path)

    @staticmethod
    def _getUrl(path):
        return '/v1/data/' + path

    def set_attributes(self, response_json):
        pass

    def getName(self):
        _, name = getParentAndBase(self.path)
        return name

    def exists(self):
        response = self.client.headHelper(self.url)
        return (response.status_code == 200)

    def create(self):
        '''Creates a directory'''
        json = {}
        response = self.client.postJsonHelper(DataDirectory._getUrl(self.path), json, False)
        if (response.status_code != 200):
            raise DataApiError("Directory creation failed: " + str(response.content))
        return response.json()['filepath']

    def delete(self, force=False):
        url = self.url
        if force:
            url += '?force=true'

        result = self.client.deleteHelper(url)
        if 'error' in result:
            raise DataApiError(result['error']['message'] if 'message' in result['error'] else result['error'])
        else:
            return True

    def file(self, name):
        return DataFile(self.client, pathJoin(self.path, name))

    def files(self):
        return self._get_directory_iterator(DataObjectType.file)

    def dir(self, name):
        return DataDirectory(self.client, pathJoin(self.path, name))

    def dirs(self):
        return self._get_directory_iterator(DataObjectType.directory)

    def list(self):
        return self._get_directory_iterator()

    def get_permissions(self):
        '''
        Returns permissions for this directory or None if it's a special collection such as
        .session or .algo
        '''
        response = self.client.getHelper(self.url)
        if response.status_code != 200:
            raise DataApiError('Unable to get permissions:' + str(response.content))
        return None

    def update_permissions(self):
        params = {}
        response = self.client.patchHelper(self.url, params)
        if response.status_code != 200:
            raise DataApiError('Unable to update permissions: ' + response.json()['error']['message'])
        return True

    def _get_directory_iterator(self, type_filter=None):
        marker = None
        first = True
        while first or (marker is not None and len(marker) > 0):
            first = False
            url = self.url
            query_params= {}
            if marker:
                query_params['marker'] = marker
            response = self.client.getHelper(url, **query_params)
            if response.status_code != 200:
                raise DataApiError("Directory iteration failed: " + str(response.content))

            responseContent = response.content
            if isinstance(responseContent, six.binary_type):
                responseContent = responseContent.decode()

            content = json.loads(responseContent)
            if 'marker' in content:
                marker = content['marker']
            else:
                marker = None

            if type_filter is DataObjectType.directory or type_filter is None:
                for d in self._iterate_directories(content):
                    yield d
            if type_filter is DataObjectType.file or type_filter is None:
                for f in self._iterate_files(content):
                    yield f

    def _iterate_directories(self, content):
        directories = []
        if 'folders' in content:
            for dir_info in content['folders']:
                d = DataDirectory(self.client, pathJoin(self.path, dir_info['name']))
                d.set_attributes(dir_info)
                directories.append(d)
        return directories

    def _iterate_files(self, content):
        files = []
        if 'files' in content:
            for file_info in content['files']:
                f = DataFile(self.client, pathJoin(self.path, file_info['filename']))
                f.set_attributes(file_info)
                files.append(f)
        return files
