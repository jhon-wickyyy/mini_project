import uuid

SESSIONS = {}

def get_current_user(request_data,SECCIONS):
    lines = request_data.split('\r\n')

    for line in lines :
        if line.startswith("Cookie:") and 'session_id=' in line:
            session_id = line.split('session_id=')[1].split(';')[0]
            username = SECCIONS.get(session_id)
            return username

    return None

def create_session(user):
    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = user['username']
    return session_id
