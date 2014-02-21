from pyramid.authentication import AuthTktAuthenticationPolicy, AuthTktCookieHelper
from bigmax.resources import MaxServer


class MultiMaxAuthTktCookieHelper(AuthTktCookieHelper):
    """
    """

    def __init__(self, *args, **kwargs):
        super(MultiMaxAuthTktCookieHelper, self).__init__(*args, **kwargs)
        self.__cookie_name__ = self.cookie_name

    def get_cookie_name(self, request):
        calculated_cookie_name = self.__cookie_name__
        if isinstance(getattr(request, 'context', None), MaxServer):
            calculated_cookie_name = '{}_{}'.format(
                request.context.__name__,
                self.__cookie_name__
            )
        return calculated_cookie_name

    def identify(self, request):
        self.cookie_name = self.get_cookie_name(request)
        return super(MultiMaxAuthTktCookieHelper, self).identify(request)

    def remember(self, request, userid, max_age=None, tokens=()):
        self.cookie_name = self.get_cookie_name(request)
        return super(MultiMaxAuthTktCookieHelper, self).remember(request, userid, max_age, tokens)

    def forget(self, request):
        self.cookie_name = self.get_cookie_name(request)
        return super(MultiMaxAuthTktCookieHelper, self).forget(request)


class MultiMaxServerAuthTktAuthenticationPolicy(AuthTktAuthenticationPolicy):
    """
    """
    def __init__(self, *args, **kwargs):
        super(MultiMaxServerAuthTktAuthenticationPolicy, self).__init__(*args, **kwargs)
        self.cookie = MultiMaxAuthTktCookieHelper(*args, **kwargs)
