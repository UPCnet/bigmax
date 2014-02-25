# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.view import forbidden_view_config

from pyramid.security import remember, forget

from pyramid_osiris import Connector
from bigmax.views.api import TemplateAPI
from bigmax.views.views import MaxServer
import logging
import re

logger = logging.getLogger('bigmax')


def real_request_url(request):
    request_scheme = re.search(r'(https?)://', request.url).groups()[0]
    if request.get('HTTP_X_VIRTUAL_HOST_URI'):
        real_scheme = re.search(r'(https?)://', request.get('HTTP_X_VIRTUAL_HOST_URI')).groups()[0]
        return request.url.replace(request_scheme, real_scheme)
    else:
        return request.url


@view_config(name='login', context=MaxServer, renderer='bigmax:templates/login.pt')
@forbidden_view_config(renderer='bigmax:templates/login.pt')
def login(context, request):
    """ The login view - pyramid_ldap enabled with the forbidden view logic.
    """
    page_title = "BIG MAX Login"
    api = TemplateAPI(context, request, page_title)
    login_url = request.resource_url(request.context, 'login')
    referrer = real_request_url(request)
    if referrer.endswith('login'):
        referrer = api.application_url  # never use the login form itself as came_from

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
                url=login_url,
                came_from=came_from,
                login=login,
                password=password,
                api=api
            )

        # Try to authenticate with Osiris, using oauth server from the context
        connector = Connector(request.registry, request.context.oauth_server, False)
        data = connector.authenticate(login, password)
        if data:
            auth_user, oauth_token = data
            headers = remember(request, auth_user)
            client = context.maxclient
            client.setActor(auth_user)
            client.setToken(oauth_token)
            client.addUser(auth_user)

        # if not successful, try again
        else:
            return dict(
                message='Login failed. Please try again.',
                url=login_url,
                came_from=came_from,
                login=login,
                password=password,
                api=api
            )

        # Store the user's oauth token in the current session
        request.session['{}_oauth_token'.format(context.__name__)] = oauth_token

        # Finally, return the authenticated view
        return HTTPFound(headers=headers, location=request.resource_url(request.context))

    return dict(
        message=message,
        url=login_url,
        came_from=came_from,
        login=login,
        password=password,
        api=api
    )


@view_config(name='logout', context=MaxServer)
def logout(context, request):
    headers = forget(request)
    return HTTPFound(location=request.resource_url(request.context), headers=headers)
