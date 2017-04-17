from nose.tools import raises
from sdelements.SDEClient import SDEClient
from responses import GET_TASK_RESPONSE
import requests_mock

@requests_mock.Mocker()
class TestGetTask(object):

    # preparing to test
    def setUp(self):
        self.sde_client = SDEClient("http://localhost/sde","admin","admin")

    def test_get_task(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', '1-T2'), json=GET_TASK_RESPONSE)
        assert GET_TASK_RESPONSE == self.sde_client.get_task('1','1-T2')

    @raises(Exception)
    def test_get_unknown_task(self, m):
        m.register_uri('GET', SDEClient.GET_TASK_URI % (self.sde_client.url, '1', 'FAILED'), status_Code=403)
        self.sde_client.get_task('1','FAILED')
