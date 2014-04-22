from pyramid.authentication import AuthTktAuthenticationPolicy, AuthTktCookieHelper
from bigmax.resources import MaxServer
from webob.cookies import CookieProfile


class MultiMaxCookieProfile(CookieProfile):
    def __init__(self, *args, **kwargs):
        self.__cookie_name__ = ''
        super(MultiMaxCookieProfile, self).__init__(*args, **kwargs)

    @property
    def cookie_name(self):
        return self.__cookie_name__

    @cookie_name.setter
    def cookie_name(self, value):
        self.__cookie_name__ = value

    def get_cookie_name(self, request):
        calculated_cookie_name = self.__cookie_name__
        if isinstance(getattr(request, 'context', None), MaxServer):
            calculated_cookie_name = '{}_{}'.format(
                request.context.__name__,
                self.__cookie_name__
            )
        return calculated_cookie_name

    def bind(self, request):
        """ Bind a request to a copy of this instance and return it"""

        selfish = CookieProfile(
            self.get_cookie_name(request),
            self.secure,
            self.max_age,
            self.httponly,
            self.path,
            self.domains,
            self.serializer,
        )
        selfish.request = request
        return selfish


class MultiMaxAuthTktCookieHelper(AuthTktCookieHelper):
    """
    """

    def __init__(self, secret, cookie_name='auth_tkt', secure=False,
                 include_ip=False, timeout=None, reissue_time=None,
                 max_age=None, http_only=False, path="/", wild_domain=True,
                 hashalg='md5', parent_domain=False, domain=None):
        super(MultiMaxAuthTktCookieHelper, self).__init__(
            secret, cookie_name=cookie_name, secure=secure, include_ip=include_ip,
            timeout=timeout, reissue_time=reissue_time, max_age=max_age,
            http_only=http_only, path=path, wild_domain=wild_domain,
            hashalg=hashalg, parent_domain=parent_domain, domain=domain)
        self.__cookie_name__ = self.cookie_name
        self.cookie_profile = MultiMaxCookieProfile(cookie_name, secure, max_age, http_only, path, self.cookie_profile.serializer)

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
