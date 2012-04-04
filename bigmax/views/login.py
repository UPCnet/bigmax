# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.url import resource_url
from pyramid.view import forbidden_view_config

from pyramid.security import remember, forget
from pyramid.settings import asbool

import datetime

from pyramid_ldap import get_ldap_connector
from bigmax.views.api import TemplateAPI
from bigmax.utils import normalize_userdn
import requests
import json


@view_config(name='login', renderer='bigmax:templates/login.pt')
@forbidden_view_config(renderer='bigmax:templates/login.pt')
def login(context, request):
    """ The login view - pyramid_who enabled with the forbidden view logic.
    """

    page_title = "BIG MAX Login"
    api = TemplateAPI(context, request, page_title)
    enable_ldap = asbool(request.registry.settings.get('enable_ldap'))

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

        # If it's the first time the user log in the system, then create the local user structure
        user = context.db.users.find_one({'username': auth_user})

        if user:
            # User exist in database, update login time and continue
            user['last_login'] = datetime.datetime.now()
            context.db.users.save(user)
        else:
            # No userid found in the database, then create an instance
            newuser = {'username': auth_user,
                       'last_login': datetime.datetime.now(),
                       'following': {'items': [], },
                       'subscribedTo': {'items': [], }
                       }
            context.db.users.save(newuser)

        OAUTH_SERVER = 'https://oauth.upc.edu'
        GRANT_TYPE = 'password'
        CLIENT_ID = 'MAX'
        SCOPE = 'widgetcli'

        username = login

        REQUEST_TOKEN_ENDPOINT = '%s/token' % (OAUTH_SERVER)

        payload = {"grant_type": GRANT_TYPE,
                   "client_id": CLIENT_ID,
                   "scope": SCOPE,
                   "username": username,
                   "password": password
                   }

        req = requests.post(REQUEST_TOKEN_ENDPOINT, data=payload, verify=False)
        response = json.loads(req.text)
        oauth_token = response.get("oauth_token")

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
