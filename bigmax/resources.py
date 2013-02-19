from pyramid.security import Everyone, Allow, Authenticated
from beaker.cache import cache_region

DEFAULT_PERMISSIONS = [(Allow, Authenticated, 'activitystream')]


class Root(object):
    __parent__ = __name__ = None
    __acl__ = [
        (Allow, Everyone, 'anonymous'),
        (Allow, u'cn=UPCnet.Plone.Admins,ou=UPCNET,ou=Groups,dc=upc,dc=edu', 'restricted'),
        (Allow, 'victor.fernandez', 'restricted'),
        (Allow, 'carles.bruguera', 'restricted'),
        (Allow, Authenticated, 'activitystream')
        ]

    def __init__(self, request):
        self.request = request
        # MongoDB:
        registry = self.request.registry
        self.db = registry.max_store
        self.__acl__ = acl_generator(getMAXSecurity(registry))


def getMAXSettings(request):
    return request.registry.max_settings


def loadMAXSettings(settings, config):
    max_ini_settings = {key.replace('max.', 'max_'): settings[key] for key in settings.keys() if 'max' in key}
    return max_ini_settings


@cache_region('long_term')
def getMAXSecurity(registry):
    client = registry.maxclient
    return client.getSecurity()


def acl_generator(security_settings):
    return [(Allow, user, 'restricted') for user in security_settings['items'][0]['roles']['Manager']] + DEFAULT_PERMISSIONS
