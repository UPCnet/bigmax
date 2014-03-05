# -*- coding: utf-8 -*-
from bigmax.resources import MaxServer
from bigmax.views.api import TemplateAPI
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk
from pyramid.settings import asbool
from pyramid.request import Response


@view_config(name="users", context=MaxServer, renderer='bigmax:templates/users.pt', permission='restricted')
def users_view(context, request):
    """
    """

    security = context.maxclient.admin.security.get()

    users = {}
    roles = ['Manager', 'NonVisible']

    for role in roles:
        for username in security[0]['roles'].get(role, []):
            users.setdefault(username, {})
            users[username][role] = True

    user_roles = [{'username': username, 'roles': [{'name': role, 'checked': user_roles.get(role, False)} for role in roles]} for username, user_roles in users.items()]

    return dict(
        api=TemplateAPI(context, request, 'Users administration'),
        roles=roles,
        users=user_roles
    )


@view_config(route_name="api_role", context=MaxServer, permission='restricted')
def api_role(context, request):
    """
    """
    role = request.params.get('role')
    user = request.params.get('username')
    value = asbool(request.params.get('value'))

    if value:
        context.maxclient.admin.security.roles[role].users[user].post()
    else:
        context.maxclient.admin.security.roles[role].users[user].delete()

    return HTTPOk()


@view_config(route_name="api_users", context=MaxServer, permission='restricted', renderer='json')
def api_users(context, request):
    """
    """
    query = request.params.get('query')

    users = context.maxclient.people.get(qs={'username': query})

    return [{'id': user['username'], 'text': user['displayName']} for user in users]
