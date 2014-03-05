from bigmax.resources import MaxServer
from bigmax.utils import normalize_userdn
from bigmax.views.api import TemplateAPI
from collections import OrderedDict
from pyramid.httpexceptions import HTTPOk
from pyramid.security import authenticated_userid
from pyramid.view import view_config


DEFAULT_WIDGET_SETTINGS = {
    "readContext": None,
    "language": "ca",
    "activitySource": "timeline",
    "activitySortOrder": "comments"
}


@view_config(context=MaxServer, renderer='bigmax:templates/activityStream.pt', permission='activitystream')
def MaxRootView(context, request):

    username = authenticated_userid(request)
    page_title = "%s's Activity Stream" % username
    api = TemplateAPI(context, request, page_title)

    maxserver_info = OrderedDict()
    maxserver_info['Max Server'] = context.max_server
    maxserver_info['Oauth Server'] = context.oauth_server

    user_properties = context.maxclient.people[':me'].get()
    user_info = OrderedDict()
    display_properties = ['username', 'displayName']
    for prop in display_properties:
        user_info[prop] = user_properties[prop]

    subscriptions = user_properties['subscribedTo']
    for subscription in subscriptions:
        subscription['selected'] = request.session.get('maxui_settings', DEFAULT_WIDGET_SETTINGS)['readContext'] == subscription['url']

    return dict(
        settings=request.session.get('maxui_settings', DEFAULT_WIDGET_SETTINGS),
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
        'domain': context.__name__,
    }

    variables.update(request.session.get('maxui_settings', DEFAULT_WIDGET_SETTINGS))
    request.response.content_type = 'text/javascript'
    return dict(variables=variables)


@view_config(name='session-update', context=MaxServer)
def session_update(context, request):

    request.session['maxui_settings'] = dict(request.params.items())
    return HTTPOk()
