import json
import requests_mock
from nose.tools import raises

from responses import GET_TASKS_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestGetTasks(object):

    def test_get_tasks_basic_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_TASKS_URI % (sde_client.url, '1'), json=GET_TASKS_RESPONSE)
        assert json.loads(GET_TASKS_RESPONSE) == sde_client.get_tasks('1')

    def test_get_tasks_token_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Token", None, None, "1234abcd")
        m.register_uri('GET', SDEClient.GET_TASKS_URI % (sde_client.url, '1'), json=GET_TASKS_RESPONSE)
        assert json.loads(GET_TASKS_RESPONSE) == sde_client.get_tasks('1')

    @raises(Exception)
    def test_get_unknown_authentication_method(self, m):
        sde_client = SDEClient("http://localhost/sde", "Unknown", None, None, None)
        m.register_uri('GET', SDEClient.GET_TASKS_URI % (sde_client.url, '1'), json=GET_TASKS_RESPONSE)
        sde_client.get_tasks('1')
