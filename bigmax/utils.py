

def normalize_userdn(dn):
    """ Extract user id (e.g. cn=victor.fernandez,ou=Users,dc=upc,dc=edu to
        victor.fernandez
    """
    return dn.split(',')[0].split('=')[1]
