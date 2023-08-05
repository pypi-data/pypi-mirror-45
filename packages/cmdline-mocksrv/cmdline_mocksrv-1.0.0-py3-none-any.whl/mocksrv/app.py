import os
import json
from sys import argv
from flask import Flask
from flask import request
from flask import abort
from werkzeug.routing import Rule

from router import resolver
from configurator import reader as config_reader
from handlers import static
from handlers import proxy
from handlers import text
from handlers import cgi


m_config = config_reader.read('./config/config.json')

app = Flask(__name__, static_folder=None, template_folder=None)

# using werkzeug routing for cathing any http method
app.url_map.add(Rule('/', endpoint='catch_query'))
app.url_map.add(Rule('/<path:path>', endpoint='catch_query'))

@app.endpoint('catch_query')
def catch_query(path=None):
    print("index")
    print(request.host_url)
    print(path)
    route = resolver.resolve(path, m_config['data'])

    if route is None:
        abort(404)

    route_type = route['type']

    if route_type == 'static':
        return static.handle(path, route['details'], route)
    elif route_type == 'proxy':
        return proxy.handle(path, route['details'], route)
    elif route_type == 'text':
        return text.handle(path, route['details'])
    elif route_type == 'cgi':
        return cgi.handle(path, route['details'], route, m_config['cgi'])

if __name__ == "__main__":
    app.run()
