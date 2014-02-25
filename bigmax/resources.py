from beaker.cache import cache_region
from maxclient import MaxClient
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import authenticated_userid

import ConfigParser


class MaxServer(dict):

    __DEFAULT_PERMISSIONS__ = (Allow, Authenticated, 'activitystream')

    def __init__(self, request, **kwargs):
        self.request = request

        self.max_server = kwargs['max_server']
        self.oauth_server = kwargs['oauth_server']
        self.oauth_grant_type = 'password'
        self.stomp_server = kwargs['stomp_server']
        self.__name__ = kwargs['name']

    @property
    def maxclient(self):
        maxclient = MaxClient(self.max_server, self.oauth_server)
        # Set authentication on max if we're authenticated on bigmax
        # otherwise return a raw maxclient
        userid = authenticated_userid(self.request)
        if userid:
            token = self.request.session.get('{}_oauth_token'.format(self.__name__), None)
            maxclient.setActor(userid)
            maxclient.setToken(token)
        return maxclient

    @property
    def __acl__(self):
        security_settings = getMAXSecurity(self.maxclient)
        for user in security_settings[0]['roles']['Manager']:
            yield (Allow, user, 'restricted')
        yield self.__DEFAULT_PERMISSIONS__

    def __resource_url__(self, request, info):
        app_url = request.application_url.rstrip('/')
        return '/'.join((app_url, self.__name__, ''))

    def __repr__(self):
        return '<MaxServer "{}" @ {}>'.format(self.__name__, self.max_server)


def get_root(request):
    instances = getInstances(request)
    return {instance["name"]: MaxServer(request, **instance) for instance in instances}


@cache_region('long_term')
def getInstances(request):
    settings = getMAXSettings(request)
    instances_file = ConfigParser.ConfigParser()
    instances_file.read(settings['max_instances'])

    instances = []
    for section in instances_file.sections():
        instances.append({
            "name": section,
            "max_server": instances_file.get(section, "max_server"),
            "stomp_server": instances_file.get(section, "stomp_server"),
            "oauth_server": instances_file.get(section, "oauth_server")
        })

    return instances


def getMAXSettings(request):
    return request.registry.max_settings


def loadMAXSettings(settings, config):
    max_ini_settings = {key.replace('max.', 'max_'): settings[key] for key in settings.keys() if 'max' in key}
    return max_ini_settings


@cache_region('long_term')
def getMAXSecurity(client):
    return client.getSecurity()
