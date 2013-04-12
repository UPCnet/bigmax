# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI

from pygments import highlight
from pygments.lexers import PythonTracebackLexer, HttpLexer
from pygments.formatters import HtmlFormatter

import re
from DateTime import DateTime


@view_config(route_name="exception", renderer='bigmax:templates/exceptions.pt', permission='restricted')
def configView(context, request):
    logfile = request.registry.settings.get('exceptions_log')
    date, http_request, traceback = re.search(r'BEGIN EXCEPTION REPORT: %s\nDATE: (.*?)\nREQUEST:\n\n(.*?)\n\nTRACEBACK:\n\n(.*?)\nEND EXCEPTION REPORT' % request.matchdict['id'], open(logfile).read(), re.DOTALL).groups()
    page_title = "BIG MAX Exception Log"
    api = TemplateAPI(context, request, page_title)
    return dict(api=api,
                date=DateTime(date).strftime('%Y/%M/%d %H:%M:%S'),
                exception_id=request.matchdict['id'],
                http_request=highlight(http_request, HttpLexer(), HtmlFormatter(style='friendly')),
                traceback=highlight(traceback, PythonTracebackLexer(), HtmlFormatter(style="friendly")),
                url='%s/exeptions' % api.application_url)
