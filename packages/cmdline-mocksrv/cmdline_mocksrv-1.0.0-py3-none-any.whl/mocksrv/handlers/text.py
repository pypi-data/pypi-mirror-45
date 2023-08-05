from flask import Response
from flask import request
import json

def get_text_response(content_obj):
    json_data = json.dumps(content_obj)
    str = json_data.strip('"')
    mimetype = 'application/json'
    if len(str) < len(json_data):
        mimetype = 'text/plain'
    return Response(str, mimetype=mimetype)


def handle(request_path, details, route):
    method = str(request.method)

    if 'var' in details:
        for rule in details['var']:
            if '_verb' in rule and rule['_verb'] != method:
                continue
            matched = True
            for name in rule.keys():
                if name == '_verb' or name == '_content':
                    continue
                else:
                    value = rule[name]
                    comps = route['path'].strip('/').split('/')
                    p_comps = request_path.strip('/').split('/')
                    current_value = None
                    for i in range(0, len(comps)):
                        if comps[i].startswith('{' + name + "}") or comps[i].startswith('{' + name + ':'):
                            current_value = p_comps[i]
                    if value != current_value:
                        matched = False
                        continue

            if matched:
                return get_text_response(rule['_content'])

    if not 'verb' in details:
         return get_text_response(details['content'])

    if not method in details['verb'].keys():
        if not '*' in details['verb'].keys():
             return get_text_response(details['content'])
        return get_text_response(details['verb']['*'])
    return get_text_response(details['verb'][method])