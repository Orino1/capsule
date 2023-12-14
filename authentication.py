import bcrypt
import secrets
from sanitization import sanitize
from engine import db
import uuid
from error import error

class SessionManager:
    SESSIONS = {}

    def generate_session_token():
        return secrets.token_hex(16)

    def delete_session(self, session):
        SessionManager.SESSIONS.pop(session, None)

    def is_authenticated(self, request):
        session = request.cookies.get('session', '')
        return SessionManager.SESSIONS.get(session) is not None

    def get_user_id(self, request):
        session = request.cookies.get('session')
        return SessionManager.SESSIONS.get(session)

    def set_user_session(self, session_key, user_id):
        SessionManager.SESSIONS[session_key] = user_id


class EmailVerification:

    def validate_email(self, verification_token):
        exists = db.token_exists(verification_token)
        if exists:
            query = 'UPDATE users SET verified = 1 WHERE email_verification_token = %s'
            params = (verification_token,)
            db.execute_query(query, params)

    def email_exists(self, email):
        return db.email_exists(email)

class PasswordReset:

    def set_password_reset_token(self, email, reset_token):
        query = "UPDATE users SET reset_token = %s WHERE email = %s"
        params = (reset_token, email)
        db.execute_query(query, params)

    def change_password(self, request, reset_token):
        if not sanitize.reset_password_form(request):
            return False

        if not db.reset_token_exists(reset_token):
            return False

        password = request.form.get('password1', '').strip()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        update_password_query = "UPDATE users SET hashed_password = %s WHERE reset_token = %s"
        update_token_query = "UPDATE users SET reset_password_token = NULL WHERE reset_token = %s"

        params = (hashed_password, reset_token)

        return db.execute_query(update_password_query, params) and db.execute_query(update_token_query, (reset_token,))


class UserRegistration:

    def register_user(self, request, verification_token):
        if not sanitize.registration_form(request):
            return False

        user_id = str(uuid.uuid4())
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        data = (user_id, username, email, hashed_password, verification_token)

        if db.email_exists(email):
            error.add_error('This email already exists')
            return False

        insert_query = f"INSERT INTO users (id, username, email, hashed_password, verification_token) VALUES (%s, %s, %s, %s, %s)"
        return db.execute_query(insert_query, data)


class UserAuthentication:


    def login_user(self, request):
        if not sanitize.login_form(request):
            return False

        email = request.form.get('email', '').lower()
        password_query = f'SELECT hashed_password, verified FROM users WHERE email = %s'
        params = (email,)

        success, result = db.query_one(password_query, params)

        if not result:
            return False

        hashed_password = result.get('hashed_password')
        verified = result.get('verified')

        provided_password = request.form.get('password', '').encode('utf-8')
        if bcrypt.checkpw(provided_password, hashed_password.encode('utf-8')) and verified:
            user_id_query = f'SELECT id FROM users WHERE email = %s'
            user_id_params = (email,)
            success, result = db.query_one(user_id_query, user_id_params)
            session = SessionManager.generate_session_token()
            SessionManager.set_user_session(session, result['id'])
            return session

        return False


class FileHandler:

    def is_allowed_file(self, filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        extension = filename.split('.')[-1]
        return extension in allowed_extensions


class Capsule:

    def add_capsule_to_db(self, request, title, image, message, open_at):
        capsule_id = str(uuid.uuid4())
        user_id = SessionManager.get_user_id(request)

        if image:
            extension = image.filename.split('.')[-1]
            image_name = f"{capsule_id}.{extension}"
            image_path = f"images/{image_name}"
            image.save(image_path)
            insert_query = "INSERT INTO capsules (capsuleid, title, user_id, image, message, open_at) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (capsule_id, title, user_id, image_path, message, open_at)
        else:
            insert_query = "INSERT INTO capsules (capsuleid, title, user_id, message, open_at) VALUES (%s, %s, %s, %s, %s)"
            params = (capsule_id, title, user_id, message, open_at)

        return db.execute_query(insert_query, params)

    def get_capsules(self, request):
        user_id = SessionManager.get_user_id(request)
        select_query = 'SELECT capsuleid, title, image, message, link FROM capsules WHERE user_id = %s AND opened = TRUE'
        params = (user_id,)
        return db.query_all(select_query, params)
    
    def create_link_for_a_capsule(self, token, capsule_id):
        query = 'UPDATE capsules SET link = %s WHERE capsuleid = %s'
        param = (token, capsule_id)
        return db.execute_query()


class Utility:

    def url_token_generator(self):
        return secrets.token_urlsafe(69)


authenticate = UserAuthentication()
verification = EmailVerification()
reset_handler = PasswordReset()
registration = UserRegistration()
file_handler = FileHandler()
capsule_handler = Capsule()
session_manager = SessionManager()
utility = Utility()
