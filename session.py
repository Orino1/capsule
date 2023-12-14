import secrets

class SessionManager:
    SESSIONS = {}

    def generate_session_token(self):
        return secrets.token_hex(16)

    def delete_session(self, session):
        self.SESSIONS.pop(session, None)

    def is_authenticated(self, request):
        session = request.cookies.get('session', '')
        return self.SESSIONS.get(session) is not None

    def get_user_id(self, request):
        session = request.cookies.get('session')
        return self.SESSIONS.get(session)

    def set_user_session(self, session_key, user_id):
        self.SESSIONS[session_key] = user_id

session_manager = SessionManager()