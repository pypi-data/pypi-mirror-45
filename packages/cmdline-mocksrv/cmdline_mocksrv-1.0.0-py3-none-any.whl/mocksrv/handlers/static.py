import os
from flask import send_file
from flask import abort


def path_replace(target, source):
    target.strip('/')
    source.strip('/')
    target_parts = target.split('/')
    source_parts = source.split('/')
    return '/'.join(target_parts[len(source_parts):]).strip('/')


def get_static_path(request_path, details, route):
    file = None

    clean_path = route['path'].strip('/')

    request_path = path_replace(request_path, clean_path)
    request_path = request_path.strip('/')
    
    # if config details path is file then any request should return this file
    if os.path.isfile(details['path']):
        file = details['path']
    # if config details path is dir then join the request string
    elif os.path.isdir(details['path']):
        file = details['path'].rstrip('/') + '/' + request_path
        # if resulting path is dir then use default file in this dir
        if os.path.isdir(file):
            file = file.rstrip('/') + '/' + details['default_file']
    return file


def handle(request_path, details, route):
    
    file = get_static_path(request_path, details, route)

    if file is None or not os.path.exists(file):
        print('Not found file at ' + file)
        abort(404)
    return send_file(file, as_attachment=details['as_attachment'])
