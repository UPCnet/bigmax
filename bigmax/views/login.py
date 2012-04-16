# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.view import forbidden_view_config

from pyramid.security import remember, forget
from pyramid.settings import asbool

from pyramid_ldap import get_ldap_connector
from bigmax.views.api import TemplateAPI
from bigmax.utils import normalize_userdn
import requests
import json
import logging


@view_config(name='login', renderer='bigmax:templates/login.pt')
@forbidden_view_config(renderer='bigmax:templates/login.pt')
def login(context, request):
    """ The login view - pyramid_who enabled with the forbidden view logic.
    """

    page_title = "BIG MAX Login"
    api = TemplateAPI(context, request, page_title)
    enable_ldap = asbool(request.registry.settings.get('enable_ldap'))
    max_settings = request.registry.max_settings
    logger = logging.getLogger('bigmax')

    login_url = resource_url(request.context, request, 'login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from

    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''

    if request.params.get('form.submitted', None) is not None:
        # identify
        login = request.POST.get('login')
        password = request.POST.get('password')

        if login is u'' or password is u'':
            return dict(
                    message='You need to suply an username and a password.',
                    url=api.application_url + '/login',
                    came_from=came_from,
                    login=login,
                    password=password,
                    api=api
                    )

        if enable_ldap:
            connector = get_ldap_connector(request)
            data = connector.authenticate(login, password)
            if data:
                dn = data[0]
                headers = remember(request, dn)
                auth_user = normalize_userdn(dn)
            # if not successful, try again
            else:
                return dict(
                        message='Login failed. Please try again.',
                        url=api.application_url + '/login',
                        came_from=came_from,
                        login=login,
                        password=password,
                        api=api
                        )
        else:
            # Harcoded developer user
            # Try to suck less here in the future...
            auth_user = "maxupcnet"
            headers = remember(request, auth_user)

        # Access the MAX API to look for the auth user
        requser = requests.post('%s/people/%s' % (max_settings.get('max_server'), auth_user), "", auth=(max_settings.get('max_ops_username'), max_settings.get('max.ops_password')))

        if requser.status_code == 201:
            logger.info("User %s created successfully in MAX server." % auth_user)
        elif requser.status_code == 200:
            logger.info("User %s logged in." % auth_user)
        else:
            logger.info("Something wrong happened while accessing MAX server and authenticating %s user." % auth_user)

        # Request token for auth user
        payload = {"grant_type": max_settings.get('max_oauth_grant_type'),
                   "client_id": max_settings.get('max_oauth_clientid'),
                   "scope": max_settings.get('oauth_scope'),
                   "username": auth_user,
                   "password": password
                   }

        req = requests.post(max_settings.get('max_oauth_token_endpoint'), data=payload, verify=False)
        response = json.loads(req.text)
        oauth_token = response.get("oauth_token")

        # Store the user's oauth token in the current session
        request.session['oauth_token'] = oauth_token

        # Finally, return the authenticated view
        return HTTPFound(headers=headers, location=came_from)

    return dict(
            message=message,
            url=api.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
            api=api
            )


@view_config(name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.resource_url(request.context), headers=headers)
