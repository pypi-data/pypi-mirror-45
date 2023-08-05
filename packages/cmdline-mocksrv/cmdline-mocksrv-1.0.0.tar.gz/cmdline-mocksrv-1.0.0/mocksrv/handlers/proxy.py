from flask import Response
from flask import request
import requests


def handle(request_path, details, route):
    url_repl = request.host_url.rstrip('/') + '/' + route['path'].strip('/')
    url = request.url.replace(url_repl, details['host'].rstrip('/'))
    #
    print('proxying to url ' + url)

    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response
