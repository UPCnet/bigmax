from bigmax.resources import MaxServer

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import pymongo
import re
import requests

SERVERS_DB = {
    'oauth.upcnet.es': {
        'hosts': "faiada.upcnet.es:27017,fajolpetit.upcnet.es:27017,finestrelles.upcnet.es:27017",
        'replica_set': "maxcluster"
    }
}


def getMongoDB(server, db_name):
    conn = pymongo.MongoReplicaSetClient(
        SERVERS_DB[server]['hosts'],
        replicaSet=SERVERS_DB[server]['replica_set'],
        use_greenlets=True)

    return conn[db_name]


def getTokenFor(server, username):
    payload = {
        "grant_type": 'password',
        "client_id": 'MAX',
        "scope": 'widgetcli',
        "username": username,
        "password": "itdoesntmatter"
    }
    resp = requests.post('{}/token-bypass'.format(server), data=payload, verify=False)
    token = resp.json()['access_token']
    return token


@view_config(context=MaxServer, name="impersonate", permission='restricted', request_method='POST')
def impersonate_view(context, request):
    """
    """
    if 'set_impersonation' in request.params.keys():
        username = request.params.get("set_impersonation", None)
        if username is not None:
            impersonated_token = getTokenFor(context.oauth_server, username)
            if impersonated_token:
                request.session['impersonated_token'] = impersonated_token
                request.session['impersonated_username'] = username

    else:
        try:
            del request.session['impersonated_username']
            del request.session['impersonated_token']
        except:
            print "Cannot cancel impersonation"
    return HTTPFound(request.resource_url(request.context, ''))
