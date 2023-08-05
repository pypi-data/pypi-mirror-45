'Aldebaran Algorithm API Client (python)'

import base64
import re
from Aldebaran.errors import ApiError, ApiInternalError
from enum import Enum
import json

OutputType = Enum('OutputType','default raw')

class Algorithm(object):
    def __init__(self, client, algoRef):
        algoRegex = re.compile(r"(?:algo://|/|)(\w+/.+)")
        m = algoRegex.match(algoRef)
        if m is not None:
            self.client = client
            self.path = m.group(1)
            self.url = '/v1/algo/' + self.path
            self.query_parameters = {}
            self.output_type = OutputType.default
            self.content_type = None
        else:
            raise ValueError('Invalid algorithm URI: ' + algoRef)

    def set_options(self, output=OutputType.default, content_type=None, **query_parameters):
        self.output_type = output
        self.query_parameters = query_parameters
        self.content_type = content_type
        return self

    def pipe(self, input1):

        if self.output_type == OutputType.raw:
            return self._postRawOutput(input1)
        else:
            return json.loads(self._postRawOutput(input1))

    def _postRawOutput(self, input1):
            self.query_parameters['output'] = 'raw'
            response = self.client.postJsonHelper(self.url, input1, parse_response_as_json=False, content_type=self.content_type, **self.query_parameters)
            if response.status_code == 400:
                raise ApiError(response.text)
            elif response.status_code == 500:
                raise ApiInternalError(response.text)
            else:
                return response.text

