# -*- coding: utf-8 -*-
from pyramid.view import view_config

from bigmax.views.api import TemplateAPI
from bigmax.resources import MaxServer
from pygments import highlight
from pygments.lexers import PythonTracebackLexer, HttpLexer
from pygments.formatters import HtmlFormatter
from pyramid.renderers import render_to_response
from DateTime import DateTime


@view_config(context=MaxServer, name="exceptions", renderer='bigmax:templates/exceptions.pt', permission='restricted')
def configView(context, request):
    page_title = "BIG MAX Exception Log"
    api = TemplateAPI(context, request, page_title)
    if request.subpath:
        template = 'bigmax:templates/exception.pt'
        exception_id = request.subpath[0]
        try:
            exception_report = context.maxclient.admin.maintenance.exceptions[exception_id].get()
        except:
            result = dict(
                api=api,
                exception_id=None)
        else:
            result = dict(
                api=api,
                date=DateTime(exception_report['date']).strftime('%Y/%M/%d %H:%M:%S'),
                exception_id=exception_id,
                http_request=highlight(exception_report['request'], HttpLexer(), HtmlFormatter(style='friendly')),
                traceback=highlight(exception_report['traceback'], PythonTracebackLexer(), HtmlFormatter(style="friendly")),
                url='%s/exeptions' % api.application_url)
    else:
        template = 'bigmax:templates/exceptions.pt'
        exceptions_list = context.maxclient.admin.maintenance.exceptions.get()
        # invert and format date
        exceptions_list = [{"id": a["id"], "date": DateTime(a['date']).strftime('%Y/%M/%d %H:%M:%S')} for a in exceptions_list[::-1]]
        result = dict(
            api=api,
            exceptions=exceptions_list)

    return render_to_response(template, result, request=request)
