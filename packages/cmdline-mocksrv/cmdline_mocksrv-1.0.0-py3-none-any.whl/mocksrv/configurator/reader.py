import json
from pathvalidate import ValidationError, validate_filename


def fill_config_defaults_static(details):
    if not 'default_file' in details:
        details['default_file'] = 'index.html'
    if not 'as_attachment' in details:
        details['as_attachment'] = False


def fill_main_config_defaults(config):
    for route in config['routes']:        
        details = route['details']
        if route['type'] == 'static':
            fill_config_defaults_static(details)


def fill_cgi_config_defaults(cgi_config):
    if 'cgi' not in cgi_config or len(cgi_config['cgi']) == 0:
        cgi_config['cgi'] = [{ 'extension': 'py', 'cmd': 'python'}]
        return

    for cgi in cgi_config['cgi']:
        if 'extension' not in cgi or 'cmd' not in cgi:
            raise Exception('Error in CGI config')
        validate_filename(cgi_config['cgi']['extension'].lstrip('.'))


def fill_config_defaults(config, cgi_config):
    fill_main_config_defaults(config)
    if len(cgi_config) == 0: 
        cgi_config['cgi'] = []
    fill_cgi_config_defaults(cgi_config)


def read_file(path):
    file = open(path, 'r')
    contents = file.read()
    return json.loads(contents)


def read(path, cgi_path=None):
    config = read_file(path)
    cgi_config = {}
    if not cgi_path is None:
        cgi_config = read_file(cgi_path)
    fill_config_defaults(config, cgi_config)
    return { 'data': config, 'cgi': cgi_config['cgi'] }
