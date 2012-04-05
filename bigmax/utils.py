import re


def normalize_userdn(dn):
    """ Extract user id (e.g. cn=victor.fernandez,ou=Users,dc=upc,dc=edu to
        victor.fernandez, or leave username intact
    """
    if dn:
        regex = r'(cn=)?([^,=]*),?'
        return re.search(regex, dn).groups()[1]
    else:
        return None
