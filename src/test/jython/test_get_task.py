import json
import requests_mock
from nose.tools import eq_, raises

from responses import GET_TASK_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestGetTask(object):

    def test_get_task_basic_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", None, "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_TASK_URI % (sde_client.url, '1', '1-T2'), json=json.loads(GET_TASK_RESPONSE))
        eq_(json.loads(GET_TASK_RESPONSE), sde_client.get_task('1', '1-T2'))

    def test_get_task_token_auth(self, m):
        sde_client = SDEClient("http://localhost/sde", "Token", None, None, None, "1234abcd")
        m.register_uri('GET', SDEClient.GET_TASK_URI % (sde_client.url, '1', '1-T2'), json=json.loads(GET_TASK_RESPONSE))
        eq_(json.loads(GET_TASK_RESPONSE), sde_client.get_task('1', '1-T2'))

    @raises(Exception)
    def test_get_unknown_task(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", None, "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_TASK_URI % (sde_client.url, '1', 'FAILED'), status_Code=403)
        sde_client.get_task('1', 'FAILED')

    @raises(Exception)
    def test_get_unknown_authentication_method(self, m):
        sde_client = SDEClient("http://localhost/sde", "Unknown", None, None, None, None)
        m.register_uri('GET', SDEClient.GET_TASK_URI % (sde_client.url, '1', '1-T2'), json=json.loads(GET_TASK_RESPONSE))
        sde_client.get_task('1', 'FAILED')
