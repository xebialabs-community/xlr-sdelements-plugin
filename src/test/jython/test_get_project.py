import json
import requests_mock
from nose.tools import eq_, raises

from responses import GET_APPLICATION_RESPONSE, GET_PROJECT_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestGetProject(object):

    def test_get_project_basic_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", None, "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1', 'Project Test'), json=json.loads(GET_PROJECT_RESPONSE))
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=json.loads(GET_APPLICATION_RESPONSE))
        eq_(json.loads(GET_PROJECT_RESPONSE)['results'][0], sde_client.get_project('Application Test', 'Project Test'))

    def test_get_project_token_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Token", None, None, None, "1234abcd")
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1', 'Project Test'), json=json.loads(GET_PROJECT_RESPONSE))
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=json.loads(GET_APPLICATION_RESPONSE))
        eq_(json.loads(GET_PROJECT_RESPONSE)['results'][0], sde_client.get_project('Application Test', 'Project Test'))

    @raises(Exception)
    def test_get_unknown_project(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", None, "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1280', 'FAILED'), status_Code=403)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=json.loads(GET_APPLICATION_RESPONSE))
        sde_client.get_project('Application Test', 'FAILED')

    @raises(Exception)
    def test_get_unknown_authentication_method(self, m):
        sde_client = SDEClient("http://localhost/sde", "Unknown", None, None, None, None)
        m.register_uri('GET', SDEClient.GET_PROJECTS % (sde_client.url, '1280', 'FAILED'), json=json.loads(GET_PROJECT_RESPONSE))
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=json.loads(GET_APPLICATION_RESPONSE))
        sde_client.get_project('Application Test', 'FAILED')
