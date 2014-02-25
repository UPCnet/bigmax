from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.response import Response
from pyramid.httpexceptions import HTTPOk

import requests
from urllib2 import urlparse

from bigmax.resources import MaxServer
from bigmax.views.api import TemplateAPI
from bigmax.utils import normalize_userdn
from collections import OrderedDict


@view_config(context=MaxServer, renderer='bigmax:templates/activityStream.pt', permission='activitystream')
def rootView(context, request):

    username = authenticated_userid(request)
    page_title = "%s's Activity Stream" % username
    api = TemplateAPI(context, request, page_title)

    maxserver_info = OrderedDict()
    maxserver_info['Max Server'] = context.max_server
    maxserver_info['Oauth Server'] = context.oauth_server

    user_properties = context.maxclient.getUser()
    user_info = OrderedDict()
    display_properties = ['username', 'displayName']
    for prop in display_properties:
        user_info[prop] = user_properties[prop]

    subscriptions = user_properties['subscribedTo']
    for subscription in subscriptions:
        subscription['selected'] = request.session['maxui_settings']['readContext'] == subscription['url']

    return dict(
        settings=request.session['maxui_settings'],
        context_url=request.resource_url(request.context, ''),
        maxserver_name=context.__name__,
        api=api,
        maxserver_info=[{'key': k, 'value': v} for k, v in maxserver_info.items()],
        user_profile=dict(
            properties=[{'key': k, 'value': v} for k, v in user_info.items()],
            subscriptions=subscriptions
        )
    )


@view_config(name='variables.js', context=MaxServer, renderer='bigmax:templates/js_variables.js.pt')
def js_variables(context, request):

    username = normalize_userdn(authenticated_userid(request))

    variables = {
        'username': username,
        'token': request.session.get('{}_oauth_token'.format(context.__name__)),
        'server': context.max_server,
        'stomp': context.stomp_server,
        'grant': context.oauth_grant_type,
        'activitySource': 'timeline',
        'activitySortOrder': 'comments',
        'language': 'ca',
        'domain': context.__name__
    }
    variables.update(request.session['maxui_settings'])
    request.response.content_type = 'text/javascript'
    return dict(variables=variables)


@view_config(name='session-update', context=MaxServer)
def session_update(context, request):

    request.session['maxui_settings'] = dict(request.params.items())
    return HTTPOk()
