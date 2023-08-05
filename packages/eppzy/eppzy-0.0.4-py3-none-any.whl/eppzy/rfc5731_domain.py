from eppzy.util import parse_iso_datetime
from eppzy.bases import EPPMapping, object_handler, extract_optional
from eppzy.check import check


@object_handler('domain', 'urn:ietf:params:xml:ns:domain-1.0')
class Domain(EPPMapping):
    def _info_response(self, resp):
        resData = self._resData(resp)
        dse = self._get_in_xmlns(self.ns_url)
        dses = self._get_all_xmlns(self.ns_url)
        i = dse(resData, 'infData')
        data = {
            'name': dse(i, 'name').text,
            'roid': dse(i, 'roid').text,
            'host': [n.text for n in dses(i, 'host')]
        }
        extract_optional(dse, i, data, 'registrant')
        extract_optional(dse, i, data, 'crDate')
        extract_optional(dse, i, data, 'exDate')
        return data

    def info(self, name, domain_pw=''):
        rootElem, d, se = self._cmd_node('info')
        se(d, 'name', attrib={'hosts': 'all'}).text = name
        ai = se(d, 'authInfo')
        se(ai, 'pw').text = domain_pw
        return (rootElem, self._info_response)

    def check(self, names):
        return check(self, names)

    def _create_response(self, resp):
        resData = self._resData(resp)
        dse = self._get_in_xmlns(self.ns_url)
        creData = dse(resData, 'creData')
        data = {
            'name': dse(creData, 'name').text,
            'created_date': parse_iso_datetime(dse(creData, 'crDate').text)}
        extract_optional(
            dse, creData, data, 'exDate', dict_name='expiry_date',
            transform=parse_iso_datetime)
        return data

    def create(
            self, name, *, period=None, period_unit='y', ns=[],
            registrant=None, contacts={}, password=None):
        rootElem, d, se = self._cmd_node('create')
        se(d, 'name').text = name
        if period:
            se(d, 'period', attrs={'unit': period_unit}).text = period
        if ns:
            raise NotImplementedError('Host bit not implemented yet')
        if registrant:
            se(d, 'registrant').text = registrant
        if contacts:
            for ctype, c in contacts.items():
                se(d, 'contact', attrs={'type': ctype}).text = c
        authInfo = se(d, 'authInfo')
        if password:
            se(authInfo, 'pw').text = password
        return (rootElem, self._create_response)

    def delete(self, name):
        rootElem, d, se = self._cmd_node('delete')
        se(d, 'name').text = name
        return (rootElem, lambda x: x)

    def _renew_response(self, resp):
        resData = self._resData(resp)
        dse = self._get_in_xmlns(self.ns_url)
        renData = dse(resData, 'renData')
        data = {'name': dse(renData, 'name').text}
        extract_optional(
            dse, renData, data, 'exDate', dict_name='new_expiry_date',
            transform=parse_iso_datetime)
        return data

    def renew(
            self, name, current_expiry_date, *, period=None,
            period_unit='y'):
        rootElem, d, se = self._cmd_node('renew')
        se(d, 'name').text = name
        se(d, 'curExpDate').text = str(current_expiry_date)
        if period:
            se(d, 'period', attrib={'unit', period_unit}).text = period
        return (rootElem, self._renew_response)
