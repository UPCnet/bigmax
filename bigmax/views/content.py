from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest

from pyramid.security import authenticated_userid

from bigmax.utils import oauth2Header
from bigmax.views.api import TemplateAPI

from bson.objectid import ObjectId

import json
import requests


#@view_config(route_name='activity', permission='restricted')
def activityView(context, request):
    activity_id = ObjectId(request.matchdict['id'])

    activity = context.db.activity.find_one(activity_id)

    return Response(str(activity))


@view_config(route_name='profiles', renderer='bigmax:templates/profile.pt', permission='restricted')
def profilesView(context, request):

    username = request.matchdict['username']
    page_title = "%s's User Profile" % username
    api = TemplateAPI(context, request, page_title)
    max_settings = request.registry.max_settings

    current_username = api.authenticatedUser
    user_token = request.session.get('oauth_token')

    # Access the MAX API to look for the auth user
    requser = requests.get('%s/people/%s' % (max_settings.get('max_server'), username), headers=oauth2Header(current_username, user_token), verify=False)

    userprofile = json.loads(requser.text)

    if not userprofile:
        return HTTPBadRequest('No such user')

    # Render follow button?
    if current_username == username:
        showFollowButton = False
        isFollowing = False
    else:
        showFollowButton = True
        # Follow status of the current user on the viewed user profile
        reqcurrent_user = requests.get('%s/people/%s' % (max_settings.get('max_server'), username), headers=oauth2Header(current_username, user_token), verify=False)
        current_user = json.loads(reqcurrent_user.text)

        isFollowing = False

        for following in current_user.get('following', None):
            if following['username'] == userprofile['username']:
                isFollowing = True
                break

    followinfo = {'showFollowButton': showFollowButton, 'isFollowing': isFollowing}

    return dict(api=api, userprofile=userprofile, followinfo=followinfo)
