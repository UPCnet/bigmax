# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI
from bigmax.resources import MaxServer

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

import requests
import urllib
import json


@view_config(context=MaxServer, route_name="endpoints", renderer='bigmax:templates/endpoints.pt', permission='restricted')
def endpoints_view(context, request):
    page_title = "BIG MAX Exception Log"
    api = TemplateAPI(context, request, page_title)

    return dict(api=api,
                url='%s/api' % api.application_url)


@view_config(context=MaxServer, route_name="endpoints_data", renderer='json', permission='restricted')
def endpoints_data(context, request):
    endpoints = context.maxclient.endpoints.get()

    endpoints_by_category = {}

    for route_name, route_info in endpoints.items():
        endpoints_by_category.setdefault(route_info['category'], [])
        endpoints_by_category[route_info['category']].append(route_info)

    sorted_categories = endpoints_by_category.keys()
    sorted_categories.sort()

    categories = []
    for category_name in sorted_categories:

        routes = []
        for route_info in endpoints_by_category[category_name]:
            routes.append({
                'route_id': route_info['id'],
                'route_name': route_info['name'],
                'route_url': route_info['url'],
                'methods': route_info['methods']
            })
        category = {
            'name': category_name,
            'id': category_name.lower().replace(' ', '-'),
            'resources': sorted(routes, key=lambda route: route['route_name'])
        }
        categories.append(category)
    return categories


@view_config(context=MaxServer, route_name="endpoints_request", renderer='json', permission='restricted', request_method='POST')
def endpoints_request(context, request):

    url = context.max_server + urllib.unquote(request.json['url'])
    for param, value in request.json['url_params'].items():
        url = url.replace(param, value)
    request_method = request.json['method'].lower()
    requester = getattr(requests, request_method)

    params = {
        'headers': request.json['headers'],
        'verify': False
    }

    if request_method == 'POST':
        params['data'] = request.json['postdata']

    response = requester(url, **params)

    if response.status_code != 501:
        pretty_json = {
            "objectType": "error",
            "error_description": "Not Implemented",
            "error": "NotImplementedError"
        }

        pretty_json = json.dumps(json.loads(response.content), indent=4)
        response_html = highlight(pretty_json, JsonLexer(), HtmlFormatter(style='friendly'))

    else:
        response_html = 'Not Implemented'

    json_response = {
        # request = highlight(exception_report['request'], HttpLexer(), HtmlFormatter(style='friendly')),
        # response_headers = highlight(exception_report['request'], HttpLexer(), HtmlFormatter(style='friendly')),
        'response_html': response_html
    }
    return json_response
