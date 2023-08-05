from eppzy.rfc5732_host import Host
from util import mocked_session, data_file_contents


def test_check():
    def checks(body):
        assert b'check' in body
        assert b'ns1.panda.io' in body
        assert b'ns2.yo.ho' in body
        return data_file_contents('rfc5732/check.xml')
    with mocked_session(checks, [Host]) as s:
        r = s['host'].check(['ns1.panda.io', 'ns2.yo.ho'])
    assert r.data['checks'] == {
        'ns1.example.com': True,
        'ns2.example2.com': False,
        'ns3.example3.com': True
    }
