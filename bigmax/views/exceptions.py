# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI
from bigmax.resources import MaxServer
from pygments import highlight
from pygments.lexers import PythonTracebackLexer, HttpLexer
from pygments.formatters import HtmlFormatter

from DateTime import DateTime


@view_config(context=MaxServer, route_name="exception", renderer='bigmax:templates/exceptions.pt', permission='restricted')
def configView(context, request):

    exception_report = context.maxclient.admin.maintenance.exceptions[request.matchdict['id']].get()
    page_title = "BIG MAX Exception Log"
    api = TemplateAPI(context, request, page_title)
    return dict(api=api,
                date=DateTime(exception_report['date']).strftime('%Y/%M/%d %H:%M:%S'),
                exception_id=request.matchdict['id'],
                http_request=highlight(exception_report['request'], HttpLexer(), HtmlFormatter(style='friendly')),
                traceback=highlight(exception_report['traceback'], PythonTracebackLexer(), HtmlFormatter(style="friendly")),
                url='%s/exeptions' % api.application_url)
