from flask import Response
from ..handlers import static
from werkzeug import Headers
import subprocess


def compose_response(data):
    heading_data_list = []
    body_seek = 0
    for i in range(0, len(data) - 1):
        if chr(data[i]) == '\n' and chr(data[i+1]) == '\n':
            body_seek = i + 2
            break
        heading_data_list.append(chr(data[i]))
    
    heading_data = ''.join(heading_data_list)
    # RFC-2616
    # https://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html#sec6.1
    hd_split = heading_data.split('\n', 1)

    if len(hd_split) < 1:
        raise Exception('bad cgi response')

    head = hd_split[0].strip('\r')

    nohead = ''
    if len(hd_split) > 1:
        nohead = hd_split[1].strip('\n')

    head_values = head.split(' ')
    if len(head_values) < 2:
        raise Exception('bad cgi head: ' + head)
    try:
        status = int(head_values[1]) # status code
    except ValueError:
        raise Exception('bad cgi status code: ' + head_values[1])

    try:
        reason = head_values.split(' ', 2)[2]
    except Exception:
        reason = ''

    headers_split = nohead.split('\n\n', 1)
    headers_str = headers_split[0]

    headers_str_list = headers_str.split('\n')
    headers = Headers()

    disposition_defined = False
    for h_str in headers_str_list:
        if ':' in h_str:
            header_list = h_str.split(':', 1)
            header_key = header_list[0].strip()
            header_value = header_list[1].strip()
            if header_key.lower() == 'content-disposition':
                disposition_defined = True
            headers.add(header_key, header_value)

    if not disposition_defined:
        headers.add('Content-Disposition', 'inline')
        
    response = Response(headers = headers, status = status)
    response.set_data(data[body_seek:].decode("utf-8") )

    return response


def handle(request_path, details, route, cgi_conf):
    file = static.get_static_path(request_path, details, route)

    for c in cgi_conf:
        if file.endswith('.' + c['extension']):
            arglist = c['cmd'].split(' ')
            arglist.append(file)
            print(arglist)
            data = subprocess.run(arglist, capture_output=True).stdout
            return compose_response(data)
