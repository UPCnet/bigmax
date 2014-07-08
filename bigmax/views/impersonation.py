from bigmax.resources import MaxServer

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import pymongo
import re
import pymysql
import requests

SERVERS_DB = {
    'oauth.upcnet.es': {
        'hosts': "faiada.upcnet.es:27017,fajolpetit.upcnet.es:27017,finestrelles.upcnet.es:27017",
        'replica_set': "maxcluster"
    }
}


def getMySQLDB(config_path):
    config = open(config_path).read()
    dbname, user, password = re.search('"PDO_DSN", "mysql:dbname=(\w+);host=localhost".*?"PDO_USER", "(\w+)".*?"PDO_PASS", "(\w+)"', config, re.MULTILINE | re.DOTALL).groups()
    return pymysql.connect('localhost', user, password, dbname)


def getMongoDB(server, db_name):
    conn = pymongo.MongoReplicaSetClient(
        SERVERS_DB[server]['hosts'],
        replicaSet=SERVERS_DB[server]['replica_set'],
        use_greenlets=True)

    return conn[db_name]


def getTokenFor(server, username):
    if server.startswith('https://oauth.upcnet.es'):
        domain = re.search(r'oauth\.upcnet\.es\/?(.*)', server).groups()[0]
        domain = domain if domain else 'upcnet'

        db = getMongoDB('oauth.upcnet.es', 'osiris_{}'.format(domain))
        token = db.tokens.find_one({'username': username}).get('token', None)

    # Assume that php oauth servers exist only in monolitic environments
    if server in ['https://oauth-test.upc.edu', 'https://oauth.upc.edu']:
        payload = {
            "grant_type": 'password',
            "client_id": 'MAX',
            "scope": 'widgetcli',
            "username": username,
            "password": "itdoesntmatter"
        }
        resp = requests.post('{}/cas-token'.format(server), data=payload, verify=False)
        token = resp.json()['oauth_token']
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
