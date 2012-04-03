from pyramid.config import Configurator

from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_who.whov2 import WhoV2AuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from bigmax.resources import Root, loadMAXSettings

import pymongo


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # Security
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    whoconfig_file = settings['whoconfig_file']
    identifier_id = 'auth_tkt'
    authn_policy = WhoV2AuthenticationPolicy(whoconfig_file, identifier_id)
    authz_policy = ACLAuthorizationPolicy()

    # App config
    config = Configurator(settings=settings,
                          root_factory=Root,
                          session_factory=my_session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)
    config.add_static_view('static', 'bigmax:static')
    config.add_static_view('css', 'bigmax:css')
    config.add_static_view('less', 'bigmax:less')
    config.add_static_view('js', 'bigmax:js')
    config.add_static_view('fonts', 'bigmax:static/fonts')
    config.add_static_view('maxui', 'bigmax:maxui')

    config.add_route('profiles', '/profiles/{username}')

    # Store in registry
    db_uri = settings['mongodb.url']
    conn = pymongo.Connection(db_uri)
    db = conn[settings['mongodb.db_name']]
    config.registry.max_store = db

    # Set MAX settings
    config.registry.max_settings = loadMAXSettings(settings, config)

    config.scan('bigmax', ignore='max.tests')

    return config.make_wsgi_app()
