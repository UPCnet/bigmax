from beaker.cache import cache_region
from maxclient.rest import MaxClient
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from bigmax.utils import normalize_userdn

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
        userid = self.authenticated_username
        if userid:
            token = self.authenticated_token
            maxclient.setActor(userid)
            maxclient.setToken(token)
        return maxclient

    @property
    def real_maxclient(self):
        maxclient = MaxClient(self.max_server, self.oauth_server)
        # Set authentication on max if we're authenticated on bigmax
        # otherwise return a raw maxclient
        userid = self.real_authenticated_username
        if userid:
            token = self.real_authenticated_token
            maxclient.setActor(userid)
            maxclient.setToken(token)
        return maxclient

    @property
    def __acl__(self):
        security_settings = getMAXSecurity(self.real_maxclient)
        if security_settings:
            for user in security_settings[0]['roles']['Manager']:
                yield (Allow, user, 'restricted')
        yield self.__DEFAULT_PERMISSIONS__

    def __resource_url__(self, request, info):
        app_url = request.headers.get('X-Virtual-Host-Uri', request.application_url).rstrip('/')
        return '/'.join((app_url, self.__name__, ''))

    def __repr__(self):
        return '<MaxServer "{}" @ {}>'.format(self.__name__, self.max_server)

    @property
    def real_authenticated_username(self):
        return normalize_userdn(authenticated_userid(self.request))

    @property
    def real_authenticated_token(self):
        return self.request.session.get('{}_oauth_token'.format(self.__name__), '')

    @property
    def authenticated_username(self):
        username = self.request.session['impersonated_username'] if self.impersonated else self.real_authenticated_username
        return normalize_userdn(username)

    @property
    def authenticated_token(self):
        return self.request.session['impersonated_token'] if self.impersonated else self.real_authenticated_token

    @property
    def impersonated(self):
        return 'impersonated_username' in self.request.session


class RootMaxServer(MaxServer):
    def __resource_url__(self, request, info):
        app_url = request.headers.get('X-Virtual-Host-Uri', request.application_url).rstrip('/')
        return '/'.join((app_url, ''))


def get_root(request):
    max_settings = getMAXSettings(request)

    instances = getInstances(request)
    root_instance_config = {
        "name": max_settings['max_server_id'],
        "max_server": max_settings['max_server'],
        "stomp_server": max_settings['max_stomp'],
        "oauth_server": max_settings['max_oauth_server']
    }
    root = RootMaxServer(request, **root_instance_config)
    for instance in instances:
        root[instance["name"]] = MaxServer(request, **instance)
    return root


@cache_region('long_term')
def getInstances(request):
    settings = getMAXSettings(request)
    instances_file = ConfigParser.ConfigParser()
    instances_file.read(settings['max_instances'])

    instances = []
    for section in instances_file.sections():
        max_server_url = instances_file.get(section, "server")
        try:
            server_info = MaxClient(max_server_url).server_info
        except:
            pass
        else:
            oauth_server_url = server_info['max.oauth_server']
            stomp_server_url = server_info.get('max.stomp_server', '{}/stomp'.format(max_server_url))

            instances.append({
                "name": section,
                "max_server": max_server_url,
                "stomp_server": stomp_server_url,
                "oauth_server": oauth_server_url
            })

    return instances


def getMAXSettings(request):
    return request.registry.max_settings


def loadMAXSettings(settings, config):
    max_ini_settings = {key.replace('max.', 'max_'): settings[key] for key in settings.keys() if 'max' in key}
    return max_ini_settings


@cache_region('long_term')
def getMAXSecurity(client):
    try:
        return client.admin.security.get()
    except:
        return []

from pyramid.response import FileResponse
import os


@view_config(route_name="maxserver_maxui_files")
def maxui_static_files(context, request):
    """
    """
    here = os.path.dirname(__file__)
    resource = os.path.join(here, 'maxui', *request.matchdict.get('filepath'))
    return FileResponse(resource, request=request)
