from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.response import Response

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
    maxserver_info['name'] = context.__name__
    maxserver_info['max_server'] = context.max_server
    maxserver_info['oauth_server'] = context.oauth_server

    return dict(
        api=api,
        maxserver_info=[{'key': k, 'value': v} for k, v in maxserver_info.items()]
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
    }
    request.response.content_type = 'text/javascript'
    return dict(variables=variables)
