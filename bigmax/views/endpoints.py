# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI
from bigmax.resources import MaxServer


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
                'methods': route_info['methods']
            })
        category = {
            'name': category_name,
            'id': category_name.lower().replace(' ', '-'),
            'resources': sorted(routes, key=lambda route: route['route_name'])
        }
        categories.append(category)
    return categories
