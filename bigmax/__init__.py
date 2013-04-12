from pyramid.config import Configurator

from pyramid.settings import asbool
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings, set_cache_regions_from_settings

from bigmax.resources import Root, loadMAXSettings

import ldap
from pyramid_ldap import groupfinder

from maxclient import MaxClient

import pymongo


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # Security
    session_factory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)

    enable_ldap = asbool(settings['enable_ldap'])
    identifier_id = 'auth_tkt'

    if enable_ldap:
        authn_policy = AuthTktAuthenticationPolicy(identifier_id, callback=groupfinder)
    else:
        authn_policy = AuthTktAuthenticationPolicy(identifier_id)

    authz_policy = ACLAuthorizationPolicy()

    # App config
    config = Configurator(settings=settings,
                          root_factory=Root,
                          session_factory=session_factory,
                          authentication_policy=authn_policy,
                          authorization_policy=authz_policy)

    # LDAP (conditional)
    if enable_ldap:
        config.include('pyramid_ldap')

        config.ldap_setup('ldaps://ldap-pre.upc.edu',
                          bind='cn=ldap.upc,ou=users,dc=upc,dc=edu',
                          passwd='conldapnexio'
                         )

        config.ldap_set_login_query(base_dn='ou=users,dc=upc,dc=edu',
                                    filter_tmpl='(cn=%(login)s)',
                                    scope=ldap.SCOPE_ONELEVEL,
                                   )

        config.ldap_set_groups_query(base_dn='ou=groups,dc=upc,dc=edu',
                                     filter_tmpl='(&(objectClass=groupOfNames)(member=%(userdn)s))',
                                     scope=ldap.SCOPE_SUBTREE,
                                     cache_period=600,
                                    )

    config.add_static_view('static', 'bigmax:static')
    config.add_static_view('stylesheets', 'bigmax:stylesheets')
    config.add_static_view('js', 'bigmax:js')
    config.add_static_view('fonts', 'bigmax:static/fonts')
    config.add_static_view('maxui', 'bigmax:maxui')

    config.add_route('profiles', '/profiles/{username}')
    config.add_route('exception', '/exceptions/{id}')

    # Store in registry
    db_uri = settings['mongodb.url']
    conn = pymongo.Connection(db_uri)
    db = conn[settings['mongodb.db_name']]
    config.registry.max_store = db

    # Set MAX settings
    config.registry.max_settings = loadMAXSettings(settings, config)

    # Set a MaxClient Facility
    config.registry.maxclient = MaxClient(config.registry.max_settings['max_server'], config.registry.max_settings['max_oauth_server'])

    config.scan('bigmax', ignore='max.tests')

    return config.make_wsgi_app()
