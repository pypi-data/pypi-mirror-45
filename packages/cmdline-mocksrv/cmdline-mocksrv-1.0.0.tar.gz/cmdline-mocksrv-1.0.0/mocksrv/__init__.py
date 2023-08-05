import os
import json
from flask import Flask
from flask import request
from flask import abort
from werkzeug.routing import Rule

from .router import resolver
from .configurator import reader as config_reader
from .handlers import static
from .handlers import proxy
from .handlers import text
from .handlers import cgi

name = 'cmdline-mocksrv'


def create_app(test_config=None):

    config_path = os.environ.get('MOCKSRV_CONFIG')
    cgi_config_path = os.environ.get('MOCKSRV_CGI_CONFIG')

    if config_path is None or not os.path.exists(config_path):
        print('MOCKSRV_CONFIG variable is empty')
        print('Please set config in MOCKSRV_CONFIG env variable')
        return

    if cgi_config_path is not None and cgi_config_path != '' and not os.path.exists(cgi_config_path):
        print('MOCKSRV_CGI_CONFIG variable not empty and file doesnt exist')
        print('set MOCKSRV_CGI_CONFIG="" to use default or provide a valid config path')
        return

    m_config = config_reader.read(config_path, cgi_config_path)
    app = Flask(__name__, static_folder=None, template_folder=None)

    # using werkzeug routing for cathing any http method
    app.url_map.add(Rule('/', endpoint='catch_query'))
    app.url_map.add(Rule('/<path:path>', endpoint='catch_query'))

    @app.endpoint('catch_query')
    def catch_query(path=''):
        route = resolver.resolve(path, m_config['data'])

        if route is None:
            abort(404)

        print('Resolved route: ' + route.get('path'))

        route_type = route['type']

        if route_type == 'static':
            return static.handle(path, route['details'], route)
        elif route_type == 'proxy':
            return proxy.handle(path, route['details'], route)
        elif route_type == 'text':
            return text.handle(path, route['details'], route)
        elif route_type == 'cgi':
            return cgi.handle(path, route['details'], route, m_config['cgi'])

    return app
