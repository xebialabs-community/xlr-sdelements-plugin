#
# Copyright 2018 XEBIALABS
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
    GET_APPLICATIONS = '%s/api/v2/applications/?name=%s'
    GET_PROJECTS = '%s/api/v2/projects/?application=%s&name=%s'
    GET_PROJECT_BY_ID = '%s/api/v2/projects/%s/'
    GET_TASK_URI = '%s/api/v2/projects/%s/tasks/%s/'
    GET_TASKS_URI = '%s/api/v2/projects/%s/tasks/'
    PRIO_HIGH = (7,8,9,10)
    PRIO_MEDIUM = (4,5,6)
    PRIO_LOW = (1,2,3)

    def __init__(self, url, authentication_method, proxy, username, password, token, trust_all = False):
        self.url = url
        self.authentication_method = authentication_method
        self.proxy = proxy
        self.username = username
        self.password = password
        self.token = token
        self.trust_all = trust_all
        if trust_all:
            from trustmanager.all_truster import TrustAllCertificates
            TrustAllCertificates.trust_all_certificates()

    def _get_request(self, request_url):
        if "Basic" == "%s" % self.authentication_method:
            return requests.get(request_url, auth=(self.username, self.password), proxies=self.proxy, verify = self.trust_all)
        elif "PAT" == "%s" % self.authentication_method:
            return requests.get(request_url, headers={'Authorization': 'token %s' % self.token}, proxies=self.proxy, verify = self.trust_all)
        else:
            raise Exception("Authentication method not found: [%s]" % self.authentication_method)

    def get_application(self, application_name):
        r = self._get_request(self.GET_APPLICATIONS % (self.url, application_name))
        r.raise_for_status()
        if len(r.json()['results']) != 1:
            raise Exception("Retrieved [%s] applications, while expecting 1 for application name [%s]" % (len(r.json()['results']), application_name))
        return r.json()['results'][0]

    def get_project(self, application_name, project_name):
        application_id = self.get_application(application_name)['id']
        r = self._get_request(self.GET_PROJECTS % (self.url, application_id, project_name))
        r.raise_for_status()
        if len(r.json()["results"]) != 1:
            raise Exception("Retrieved [%s] projects, while expecting 1 for project name [%s]" % (len(r.json()["results"]), project_name))
        return r.json()["results"][0]

    def get_project_by_id(self, project_id):
        r = self._get_request(self.GET_PROJECT_BY_ID % (self.url, project_id))
        r.raise_for_status()
        return r.json()

    def get_task(self, project_id, task_id):
        r = self._get_request(self.GET_TASK_URI % (self.url, project_id, task_id))
        r.raise_for_status()
        return r.json()

    def get_tasks(self, project_id):
        r = self._get_request(self.GET_TASKS_URI % (self.url, project_id))
        r.raise_for_status()
        return r.json()

    def check_vulnerabilities(self, application, project, high, medium, low):
        proj = self.get_project(application, project)
        tasks = self.get_tasks(proj["id"])
        result = {}
        if len(tasks["results"]) == 0: return {'highResult':0,'mediumResult':0,'lowResult':0,'success':True}
        count_high = sum(task["priority"] in self.PRIO_HIGH for task in tasks["results"])
        count_open_high = sum(task["priority"] in self.PRIO_HIGH and task["status"] == "TS2" for task in tasks["results"])
        count_medium = sum(task["priority"] in self.PRIO_MEDIUM for task in tasks["results"])
        count_open_medium = sum(task["priority"] in self.PRIO_MEDIUM and task["status"] == "TS2" for task in tasks["results"])
        count_low = sum(task["priority"] in self.PRIO_LOW for task in tasks["results"])
        count_open_low = sum(task["priority"] in self.PRIO_LOW and task["status"] == "TS2" for task in tasks["results"])
        result['highResult'] = 0 if count_high == 0 else count_open_high*100/count_high
        result['mediumResult'] = 0 if count_medium == 0 else count_open_medium*100/count_medium
        result['lowResult'] = 0 if count_low == 0 else count_open_low*100/count_low
        if result['highResult'] > high or result['mediumResult'] > medium or result['lowResult'] > low:
            result['success'] = False
        else:
            result['success'] = True
        return result

    def check_risk_policy_compliant(self, project_id):
        return self.get_project_by_id(project_id)

