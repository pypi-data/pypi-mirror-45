import logging
import random
import string
import socket
import flask
import requests
from flask import _app_ctx_stack
from flask import current_app
from flask import g
from flask import request
from py_zipkin import zipkin
from py_zipkin import Encoding



__version_info__ = ('0', '0', '5')
__version__ = '.'.join(__version_info__)
__author__ = 'Hyper Anna'
__license__ = 'BSD'
__copyright__ = '(c) 2019 by Hyper Anna'
__all__ = ['Zipkin']


class Zipkin(object):

    def _gen_random_id(self):
        return ''.join(
            random.choice(
                string.digits) for i in range(16))

    def __init__(self, app=None, sample_rate=100, timeout=1):
        self._exempt_views = set()
        self._sample_rate = sample_rate
        if app is not None:
            self.init_app(app)
        self._transport_handler = None
        self._transport_exception_handler = None
        self._timeout = timeout
        self._header = {'Content-Type': 'application/json'}
        self._encoding = Encoding.V2_JSON

    def default_exception_handler(self, ex):
        pass

    def default_handler(self, encoded_span):
        try:
            #body = str.encode('\x0c\x00\x00\x00\x01') + encoded_span
            return requests.post(
                self.app.config.get('ZIPKIN_DSN'),
                data=encoded_span,
                headers=self._header,
                timeout=self._timeout,
            )
        except Exception as e:
            if self._transport_exception_handler:
                self._transport_exception_handler(e)
            else:
                self.default_exception_handler(e)

    def transport_handler(self, callback):
        self._transport_handler = callback
        return callback

    def transport_exception_handler(self, callback):
        self._transport_exception_handler = callback
        return callback

    def init_app(self, app):
        self.app = app
        app.before_request(self._before_request)
        app.after_request(self._after_request)
        self._disable = app.config.get(
            'ZIPKIN_DISABLE', app.config.get('TESTING', False))
        return self

    def _should_use_token(self, view_func):
        return (view_func not in self._exempt_views)

    def _before_request(self):
        if self._disable:
            return

        _app_ctx_stack.top._view_func = \
            current_app.view_functions.get(request.endpoint)

        if not self._should_use_token(_app_ctx_stack.top._view_func):
            return
        headers = request.headers
        trace_id = headers.get('X-B3-TraceId') or self._gen_random_id()
        span_id = headers.get('X-B3-SpanId') or self._gen_random_id()
        parent_span_id = headers.get('X-B3-ParentSpanId')
        is_sampled = str(headers.get('X-B3-Sampled') or '1') == '1'
        flags = headers.get('X-B3-Flags')

        zipkin_attrs = zipkin.ZipkinAttrs(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            flags=flags,
            is_sampled=is_sampled,
        )

        handler = self._transport_handler or self.default_handler

        span = zipkin.zipkin_span(
            service_name=self.app.config.get('ZIPKIN_SERVICE_NAME', self.app.name),
            span_name='{0}.{1}'.format(request.endpoint, request.method),
            transport_handler=handler,
            sample_rate=self._sample_rate,
            zipkin_attrs=zipkin_attrs,
            encoding=self._encoding
        )
        g._zipkin_span = span
        g._zipkin_span.start()
        default_tags = self.app.config.get('ZIPKIN_TAGS', {'env': 'Undefined', 'hostname': socket.gethostname()})
        self.update_tags(default_tags)

    def exempt(self, view):
        view_location = '{0}.{1}'.format(view.__module__, view.__name__)
        self._exempt_views.add(view_location)
        return view

    def _after_request(self, response):
        if self._disable:
            return response
        if not hasattr(g, '_zipkin_span'):
            return response
        g._zipkin_span.stop()
        return response

    def create_http_headers_for_new_span(self):
        if self._disable:
            return dict()
        return zipkin.create_http_headers_for_new_span()


    def update_tags(self, tags):
        if all([hasattr(g, '_zipkin_span'),
                g._zipkin_span]):
            g._zipkin_span.update_binary_annotations(
                tags)


def child_span(f):
    def decorated(*args, **kwargs):
        span = zipkin.zipkin_span(
            service_name=flask.current_app.name,
            span_name=f.__name__,
        )
        kwargs['span'] = span
        with span:
            val = f(*args, **kwargs)
            span.update_binary_annotations({
                'function_args': args,
                'function_returns': val,
            })
            return val

    return decorated
