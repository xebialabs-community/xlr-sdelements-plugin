from nose.tools import raises
from sdelements.SDEClient import SDEClient
from responses import GET_TASK_RESPONSE
import requests_mock

@requests_mock.Mocker()
class TestGetTask(object):

    # preparing to test
    def setUp(self):


    def test_get_task_basic_auth(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', '1-T2'), json=GET_TASK_RESPONSE)
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        assert GET_TASK_RESPONSE == sde_client.get_task('1','1-T2')

    def test_get_task_token_auth(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', '1-T2'), json=GET_TASK_RESPONSE)
        sde_client = SDEClient("http://localhost/sde", "Token", None, None, "1234abcd")
        assert GET_TASK_RESPONSE == sde_client.get_task('1','1-T2')

    @raises(Exception)
    def test_get_unknown_task(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', 'FAILED'), status_Code=403)
        sde_client = SDEClient("http://localhost/sde", "Basic", "admin", "admin", None)
        sde_client.get_task('1','FAILED')

    @raises(Exception)
    def test_get_unknown_authentication_method(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', '1-T2'), json=GET_TASK_RESPONSE)
        sde_client = SDEClient("http://localhost/sde", "Unknown", None, None, None)
        sde_client.get_task('1','FAILED')
