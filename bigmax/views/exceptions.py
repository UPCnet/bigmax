# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI
from bigmax.resources import MaxServer
from pygments import highlight
from pygments.lexers import PythonTracebackLexer, HttpLexer
from pygments.formatters import HtmlFormatter

from DateTime import DateTime


@view_config(context=MaxServer, name="exceptions", renderer='bigmax:templates/exceptions.pt', permission='restricted')
def configView(context, request):
    page_title = "BIG MAX Exception Log"
    api = TemplateAPI(context, request, page_title)

    if request.subpath:
        exception_id = request.subpath[0]
        try:
            exception_report = context.maxclient.admin.maintenance.exceptions[exception_id].get()
        except:
            return dict(
                api=api,
                exception_id=None)
        else:
            return dict(
                api=api,
                date=DateTime(exception_report['date']).strftime('%Y/%M/%d %H:%M:%S'),
                exception_id=exception_id,
                http_request=highlight(exception_report['request'], HttpLexer(), HtmlFormatter(style='friendly')),
                traceback=highlight(exception_report['traceback'], PythonTracebackLexer(), HtmlFormatter(style="friendly")),
                url='%s/exeptions' % api.application_url)
