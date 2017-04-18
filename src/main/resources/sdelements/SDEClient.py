#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests

class SDEClient:
    """
    Note: In all the API calls:
    - a 'project' arg variable is the project id
    - a 'task' arg variable is in the format <project_id>-<task_id>
        e.g. '127-T106'
    """
    GET_TASK_URI = '%s/api/v2/projects/%s/tasks/%s/'

    def __init__(self, url, authentication_method, username, password, token):
        self.url = url
        self.authentication_method = authentication_method
        self.username = username
        self.password = password
        self.token = token

    def _get_request(self, request_url):
        if self.authentication_method == 'Basic':
            return requests.get(request_url, auth=(self.username, self.password))
        elif self.authentication_method == 'Token':
            return requests.get(request_url, headers={'Authorization': 'token %s' % self.token})
        else:
            raise Exception("Authentication method not found: [%s]" % self.authentication_method)

    def get_task(self, project_id, task_id):
        r = self._get_request(self.GET_TASK_URI % (self.url, project_id, task_id))
        if r.status_code != 200:
            raise Exception("Could not get task for project [%s] with task id [%s]" % (project_id, task_id))
        return r.json()
