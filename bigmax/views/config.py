from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from bigmax.views.api import TemplateAPI

DEFAULT_OAUTH_CHECK_ENDPOINT = 'https://oauth.upc.edu/checktoken'
DEFAULT_OAUTH_GRANT_TYPE = 'password'
DEFAULT_MAX_SERVER = 'https://max.upc.edu'
DEFAULT_MAX_USERNAME = 'operations'
DEFAULT_MAX_PASSWORD = 'operations'


# Config view in da fridge!
@view_config(name="control_panel", renderer='bigmax:templates/config.pt', permission='restricted')
def configView(context, request):
    page_title = "BIG MAX Server Config"
    api = TemplateAPI(context, request, page_title)
    success = False

    config = context.db.config.find_one()
    if not config:
        config = dict(oauth_check_endpoint=DEFAULT_OAUTH_CHECK_ENDPOINT,
                      oauth_grant_type=DEFAULT_OAUTH_GRANT_TYPE,
                      max_server=DEFAULT_MAX_SERVER,
                      max_ops_username=DEFAULT_MAX_USERNAME,
                      max_ops_password=DEFAULT_MAX_PASSWORD,)

    if request.params.get('form.submitted', None) is not None:
        config['max_oauth_check_endpoint'] = request.POST.get('oauth_check_endpoint')
        config['max_oauth_grant_type'] = request.POST.get('oauth_grant_type')
        config['max_server'] = request.POST.get('max_server')
        config['max_max_ops_username'] = request.POST.get('max_ops_username')
        config['max_max_ops_password'] = request.POST.get('max_ops_password')

        # Save config data
        context.db.config.save(config)
        success = True

    if request.params.get('form.cancelled', None) is not None:
        return HTTPFound(request.application_url)

    return dict(api=api, url='%s/control_panel' % api.application_url,
                oauth_check_endpoint=config.get('max_oauth_check_endpoint', DEFAULT_OAUTH_CHECK_ENDPOINT),
                oauth_grant_type=config.get('max_oauth_grant_type', DEFAULT_OAUTH_GRANT_TYPE),
                max_server=config.get('max_server', DEFAULT_MAX_SERVER),
                max_ops_username=config.get('max_max_ops_username', DEFAULT_MAX_USERNAME),
                max_ops_password=config.get('max_max_ops_password', DEFAULT_MAX_PASSWORD),
                success=success
                )
