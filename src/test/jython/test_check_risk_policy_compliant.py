import json
import requests_mock

from nose.tools import eq_
from responses import GET_PROJECT_BY_ID_RESPONSE
from sdelements.SDEClient import SDEClient


@requests_mock.Mocker()
class TestCheckRiskPolicyCompliant(object):

    def test_check_vulnerabilities_ok(self, m):
        sde_client = SDEClient("http://localhost/sde", "Basic", None, "admin", "admin", None)
        m.register_uri('GET', SDEClient.GET_PROJECT_BY_ID % (sde_client.url, '1'), json=json.loads(GET_PROJECT_BY_ID_RESPONSE))
        result = sde_client.check_risk_policy_compliant("1")
        eq_(result['name'],"Project Test")
        eq_(result['risk_policy_compliant'],True)
