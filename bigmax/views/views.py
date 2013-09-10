from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.security import authenticated_userid
from pyramid.response import Response

import requests
from urllib2 import urlparse

from bigmax.resources import Root
from bigmax.views.api import TemplateAPI
from bigmax.utils import normalize_userdn


@view_config(context=Root, renderer='bigmax:templates/activityStream.pt', permission='activitystream')
def rootView(context, request):

    username = authenticated_userid(request)
    page_title = "%s's Activity Stream" % username
    api = TemplateAPI(context, request, page_title)
    client = request.registry.maxclient

    client.setActor(username)
    client.setToken(request.session['oauth_token'])

    subscribed = client.subscribed()

    return dict(api=api, subscribed=subscribed)


# @view_config(route_name="wadl", context=Root)
# def WADLView(context, request):

#     renderer = 'max:templates/wadl.pt'
#     response = render_to_response(renderer,
#                               dict(wadl=WADL),
#                               request=request)
#     response.content_type = 'application/xml'
#     return response


@view_config(name='variables.js', context=Root, renderer='bigmax:templates/js_variables.js.pt')
def js_variables(context, request):

    username = normalize_userdn(authenticated_userid(request))
    config = request.registry.max_settings

    variables = {'username': username,
                'token': request.session.get('oauth_token'),
                'server': config.get('max_server'),
                'stomp': config.get('max_stomp'),
                'grant': config.get('max_oauth_grant_type'),
    }
    request.response.content_type = 'text/javascript'
    return dict(variables=variables)


@view_config(name='makeRequest', context=Root)
def makeRequest(context, request):
    method = request.params.get('httpMethod')
    url = request.params.get('url')
    headers_qs = request.params.get('headers', '')
    headers = dict(urlparse.parse_qsl(headers_qs))
    data = request.params.get('postData')

    requester = getattr(requests, method.lower())
    resp = requester(url, headers=headers, data=data)

    response = Response(resp.text)
    response.status_int = resp.status_code
    response.headers.update(resp.headers)
    print 'finished'
    return response
