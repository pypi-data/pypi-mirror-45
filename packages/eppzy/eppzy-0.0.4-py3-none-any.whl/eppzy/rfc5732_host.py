from .bases import EPPMapping, object_handler, extract_optional
from .check import check


@object_handler('host', 'urn:ietf:params:xml:ns:host-1.0')
class Host(EPPMapping):
    def check(self, hosts):
        return check(self, hosts)
