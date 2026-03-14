import uuid

SESSION = {}

def create_id(user_id):
     session_id = str(uuid.uuid4())
     SESSION[session_id] = user_id
     return session_id

def get_current_user(session_id):
    user_id = SESSION.get(session_id)
    if user_id:
         return user_id
    else:
         return None