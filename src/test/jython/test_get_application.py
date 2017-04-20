import json
import requests_mock
from nose.tools import raises

from responses import GET_APPLICATION_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestGetApplication(object):

    def test_get_application_basic_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=GET_APPLICATION_RESPONSE)
        assert json.loads(GET_APPLICATION_RESPONSE)['results'][0] == sde_client.get_application('Application Test')

    def test_get_application_token_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Token", None, None, "1234abcd")
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'Application Test'), json=GET_APPLICATION_RESPONSE)
        assert json.loads(GET_APPLICATION_RESPONSE)['results'][0] == sde_client.get_application('Application Test')

    @raises(Exception)
    def test_get_unknown_application(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'FAILED'), status_Code=403)
        sde_client.get_application('FAILED')

    @raises(Exception)
    def test_get_unknown_authentication_method(self, m):
        sde_client = SDEClient("http://localhost/sde", "Unknown", None, None, None)
        m.register_uri('GET', SDEClient.GET_APPLICATIONS % (sde_client.url, 'FAILED'), json=GET_APPLICATION_RESPONSE)
        sde_client.get_application('FAILED')
