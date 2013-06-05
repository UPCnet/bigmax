import re


# For LDAP use
def normalize_userdn(dn):
    """ Extract user id (e.g. cn=victor.fernandez,ou=Users,dc=upc,dc=edu to
        victor.fernandez, or leave username intact
    """
    if dn:
        regex = r'(cn=)?([^,=]*),?'
        return re.search(regex, dn).groups()[1]
    else:
        return None


def oauth2Header(username, token):
    return {"X-Oauth-Token": token, "X-Oauth-Username": username, "X-Oauth-Scope": "widgetcli"}
