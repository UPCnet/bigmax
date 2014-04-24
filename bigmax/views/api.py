from pyramid.security import authenticated_userid
from pyramid.renderers import get_renderer
from bigmax.utils import normalize_userdn


class TemplateAPI(object):

    def __init__(self, context, request, page_title=None):
        self.context = context
        self.request = request

    @property
    def masterTemplate(self):
        master = get_renderer('bigmax:templates/master.pt').implementation()
        return master

    @property
    def impersonatedUser(self):
        return self.request.session['impersonated_username'] if self.impersonated else self.authenticatedUser

    @property
    def impersonatedUserToken(self):
        return self.request.session['impersonated_token'] if self.impersonated else self.authenticatedUserToken

    @property
    def authenticatedUser(self):
        return normalize_userdn(authenticated_userid(self.request))

    @property
    def authenticatedUserToken(self):
        return self.request.session['{}_oauth_token'.format(self.context.__name__)]

    _snippets = None

    @property
    def snippets(self):
        if self._snippets is None:
            self._snippets = get_renderer('bigmax:templates/snippets.pt').implementation()
        return self._snippets

    _status_message = None

    def getStatusMessage(self):
        if self._status_message:
            return self._status_message
        return self.request.session.pop_flash('info')

    def setStatusMessage(self, value):
        self._status_message = value

    statusMessage = property(getStatusMessage, setStatusMessage)

    _error_message = None

    def getErrorMessage(self):
        if self._error_message:
            return self._error_message
        return self.request.params.get("errorMessage", None)

    def setErrorMessage(self, value):
        self._error_message = value

    errorMessage = property(getErrorMessage, setErrorMessage)

    @property
    def application_url(self):
        app_url = self.request.application_url
        vh = self.getVirtualHost()
        if vh:
            return vh
        else:
            return app_url

    @property
    def context_url(self):
        try:
            return self.request.resource_url(self.request.context, '').rstrip('/')
        except:
            return self.application_url

    def getVirtualHost(self):
        return self.request.headers.get('X-Virtual-Host-Uri', None)

    @property
    def show_user_contexts(self):
        return self.request.view_name == u''

    @property
    def impersonated(self):
        return 'impersonated_username' in self.request.session
