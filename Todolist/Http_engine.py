import urllib.parse

def handle_request_url(raw_request_data):
    request_line = raw_request_data.split('\n',1)
    parts = request_line[0].split(' ')

    if (len(parts) >= 2):
        method = parts[0]
        raw_url = parts[1]
    else:
        method = parts[0]
        path = '/'
        parse_params = ' '
        return method, path,parse_params

    parsed_url = urllib.parse.urlparse(raw_url)
    path = parsed_url.path
    parse_params = urllib.parse.parse_qs(parsed_url.query)
    return method, path, parse_params

def handle_request_body(raw_request_data):
    parts = raw_request_data.split('\r\n\r\n',1)
    if len(parts) > 1 and parts[1]:
        body_parms = urllib.parse.parse_qs(parts[1])
        return body_parms
    return None

def get_session_id(raw_request_data):
    lines = raw_request_data.split('\n')
    for line in lines:
        if line.startswith("Cookie:") and 'session_id=' in line:
            session_id = line.split('session_id=')[1].split(';')[0].strip()
            return session_id

    return None