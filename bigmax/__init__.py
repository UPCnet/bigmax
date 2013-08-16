from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from bigmax.resources import Root, loadMAXSettings

from maxclient import MaxClient


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # Security
    session_factory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    identifier_id = 'auth_tkt'

    authn_policy = AuthTktAuthenticationPolicy(identifier_id)

    authz_policy = ACLAuthorizationPolicy()

    # App config
    config = Configurator(settings=settings,
                          root_factory=Root,
                          session_factory=session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    settings = config.registry.settings

    config.include('pyramid_osiris')
    config.osiris_setup(settings.get('max.oauth_server'), legacy_mode=settings.get('max.oauth_standard', False))

    config.add_static_view('static', 'bigmax:static')
    config.add_static_view('stylesheets', 'bigmax:stylesheets')
    config.add_static_view('js', 'bigmax:js')
    config.add_static_view('bootstrap', 'bigmax:bootstrap')
    config.add_static_view('fonts', 'bigmax:static/fonts')
    config.add_static_view('maxui', 'bigmax:maxui')

    config.add_route('profiles', '/profiles/{username}')
    config.add_route('exception', '/exceptions/{id}')

    # Set MAX settings
    config.registry.max_settings = loadMAXSettings(settings, config)

    # Set a MaxClient Facility
    config.registry.maxclient = MaxClient(config.registry.max_settings['max_server'], config.registry.max_settings['max_oauth_server'])

    config.scan('bigmax')

    return config.make_wsgi_app()
