import xml.etree.ElementTree as ET
from contextlib import contextmanager

from .rfc5731_domain import Domain
from .rfc5733_contact import Contact
from .session import RequestWrapper
from .connection import LengthPrefixed, connect


class NominateProto(LengthPrefixed):
    '''Be warned, nominate do a request/response kind of EPP, so a lone recv
    will stall

    Also the requests are 1 per connection'''

    def __init__(self, host, port):
        super().__init__(None)
        self._host = host
        self._port = port

    def send(self, b):
        assert self._s is None
        self._s = connect(self._host, self._port)
        b = b.replace(b'\n', b'')
        b += b'\n'
        self._s.send(b)

    def recv(self):
        assert self._s is not None
        r = super().recv()
        self._s.close()
        self._s = None
        return r


def nominateify(cls, clid, pw):
    class Nominated(cls):
        def _mk_request(self, xml, response_data_extractor):
            cmd = xml.find('command')
            extn = self._ensure_node(cmd, 'extension')
            loginExt = ET.SubElement(extn, 'client:data')
            ET.SubElement(loginExt, 'id').text = clid
            ET.SubElement(loginExt, 'pw').text = pw
            return super()._mk_request(xml, response_data_extractor)
    return Nominated


class N8Contact(Contact):
    def domain_info(self, domain, contact_type='o'):
        rootElem, c, se = self._cmd_node('info')
        se(c, 'id').text = 'ignored'
        cmd = rootElem.find('command')
        extn = self._ensure_node(cmd, 'extension')
        cl = se(extn, 'data')
        ET.SubElement(cl, 'domain').text = domain
        ET.SubElement(cl, 'type').text = contact_type
        return (rootElem, self._info_response)


def contact_for_domain(nom_sess, domain):
    '''The mechanism to retrieve the contact info for a domain differs
    depending on registry implementation things (which are due to change during
    2019), this abstracts the faff'''
    # .org .biz -> contact contains a roid
    # .com - blank roid - have to look up by domain and type instead
    di = nom_sess['domain'].info(domain)
    contact_roid = di.data.get('registrant')
    if contact_roid:
        return nom_sess['contact'].info(contact_roid, 'pass')
    else:
        return nom_sess['contact'].domain_info(domain)


@contextmanager
def nominate_session(host, port, client_id, password):
    proto = NominateProto(host, port)
    n = lambda cls: RequestWrapper(
        nominateify(cls, client_id, password)(proto))
    yield {
        'domain': n(Domain),
        'contact': n(N8Contact)
    }
