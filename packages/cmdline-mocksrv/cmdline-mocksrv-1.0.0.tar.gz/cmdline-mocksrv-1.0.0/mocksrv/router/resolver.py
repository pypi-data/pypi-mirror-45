def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def split_path(path):
    return list(filter(None, path.split('/')))


def check_braces(path):
    braces = []
    for symb in path:
        if symb == '{':
            braces.append('{')
        elif symb == '}':
            if len(braces) == 0:
                raise Exception('invalid route in config')
            braces.pop()
    if len(braces) != 0:
        raise Exception('invalid route in config')


def pattern_match(pattern, value):
    if not pattern.startswith('{') or not pattern.endswith('}') or pattern.count(':') > 1 or pattern.count('/') > 0:
        raise Exception('Invalid pattern. pattern: ' + pattern)

    parts = pattern.strip('{}').split(':')
    if len(parts) == 1:
        return True

    restriction = parts[1].lower()
    if restriction == 'number':
        return value.lstrip('-').isdigit()
    elif restriction == 'text':
        return True
    elif restriction == 'ascii':
        return is_ascii(value)


def resolve(path, config, depth=0):
    if depth > 5:
        raise Exception('Too many map redirects in config')
    best_route = None
    path_parts = split_path(path)

    best_len = -1
    for route in config['routes']:
        route_parts = split_path(route['path'])
        if len(route_parts) > len(path_parts):
            continue
        common_len = 0
        match = True
        for i in range(0, len(route_parts)):
            if route_parts[i] == path_parts[i] or route_parts[i].startswith('{'):
                if route_parts[i].startswith('{') and not pattern_match(route_parts[i], path_parts[i]):
                    match = False
                common_len = common_len + 1
            else:
                match = False

        if match and common_len > best_len:
            best_len = common_len
            best_route = route

    if best_route is not None and best_route['type'] == 'map':
        best_parts = split_path(best_route['path'])
        new_path = '/'.join(split_path(best_route['details']['to']) + path_parts[best_len:])
        return resolve(new_path, config, depth+1)
    return best_route


def validate_config(config):
    for route in config['routes']:
        check_braces(route['path'])
