"""
Module: authentication_handler

This module provides an AuthenticationHandler class for user registration, login, and session management.

Dependencies:
    - bcrypt: Used for password hashing.
    - secrets: Used for generating secure session tokens.
    - sanitization: Module for form input sanitization.
    - engine.db: Database module for executing queries.
    - uuid: Used for generating unique user IDs.

Classes:
    - AuthenticationHandler: Handles user authentication, registration, login, and session management.

Usage Example:
    authenticate = AuthenticationHandler()
"""

import bcrypt
import secrets
from sanitization import sanitize
from engine import db
import uuid


class AuthenticationHandler():
    """
    AuthenticationHandler Class

    This class handles user authentication, registration, login, and session management.

    Attributes:
        __usersTable (str): The name of the users table in the database.
        __sessions (dict): A dictionary to store active sessions.

    Methods:
        - genSessions(): Generates a secure session token.
        - registerUser(request): Registers a new user based on the provided registration form.
        - loginUser(request): Logs in a user based on the provided login form.
        - deleteSession(session): Deletes a session, effectively logging out the user.
        - isAuthenticated(request): Checks if a user is authenticated based on the provided request.
        - validUser(request): Validates user credentials.
        - getId(request): Retrieves the user ID associated with the current session.

    Usage Example:
        authenticate = AuthenticationHandler()
    """

    __usersTable = 'users'
    __sessions = {}

    def genSessions(self):
        """
        Generates a secure session token using secrets module.

        Returns:
            str: A session token.
        """
        return secrets.token_hex(16)

    def validateEmail(self, token):
        """

        """
        exists = db.tokenExists(token)
        if exists:
            query = 'UPDATE users SET verified = 1 WHERE token = %s'
            param = (token,)
            db.insert(query, param)

    def setPassResetToken(self, email, token):
        query = "UPDATE users SET resetpass = %s WHERE email = %s"
        param = (token, email)
        db.insert(query, param)

    def changePass(self, request, token):
        errors = sanitize.resetPassForm(request)
        if errors != []:
            return errors
        if not db.resetTokenExists(token):
            return ['No user Found please check your link']
        password = request.form.get('password1', '').strip()
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE users SET hashed_password = %s WHERE resetpass = %s"
        param = (hashedPassword, token)
        db.insert(query, param)
        query = "UPDATE users SET resetpass = NULL WHERE resetpass = %s"
        param = (token,)
        db.insert(query, param)
        return []

    def email(self, email):
        """
        """
        return db.emailExists(email)

    def registerUser(self, request, token):
        """
        registerUser(request)

        Registers a new user based on the provided registration form.

        Args:
            request: The request object containing user registration details.

        Returns:
            list of errors or empty list: List of errors if registration fails, empty list otherwise.
        """
        errors = sanitize.registrationForm(request)
        if errors != []:
            return errors
        id = str(uuid.uuid4())
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # Remember you should make the database clean out any unverefied emails every 1h
        data = (
            id,
            username,
            email,
            hashedPassword,
            token
        )
        query = f"INSERT INTO {AuthenticationHandler.__usersTable} (id, username, email, hashed_password, token) VALUES (%s, %s, %s, %s, %s)"
        return db.insertUser(query, data)

    def loginUser(self, request):
        """
        Logs in a user based on the provided login form.

        Args:
            request: The request object containing user login details.

        Returns:
            str or list of errors: Session token if login is successful, list of errors otherwise.
        """
        errors = sanitize.loginForm(request)
        if errors != []:
            return errors
        if self.validUser(request):
            query = f'SELECT id FROM {AuthenticationHandler.__usersTable} where email = %s'
            param = (request.form.get('email'.lower()),)
            id = db.queryOne(query, param)
            if isinstance(id, list):
                return ['An error occurred']
            session = self.genSessions()
            self.__sessions[session] = id
            return session
        return ['Check your email/password']

    def deleteSession(self, session):
        """
        Deletes a session, effectively logging out the user.

        Args:
            session: The session token to be deleted.
        """
        AuthenticationHandler.__sessions.pop(session, None)

    def isAuthenticated(self, request):
        """
        Checks if a user is authenticated based on the provided request.

        Args:
            request: The request object.

        Returns:
            bool: True if authenticated, False otherwise.
        """
        session = request.cookies.get('session', '')
        if AuthenticationHandler.__sessions.get(session) != None:
            return True
        return False

    def validUser(self, request):
        """
        validUser(request)

        Validates user credentials.

        Args:
            request: The request object containing user login details.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        query = f'SELECT hashed_password, verified FROM {AuthenticationHandler.__usersTable} WHERE email = %s'
        param = (request.form.get('email', '').lower(),)

        result = db.queryOne(query, param)
        if isinstance(result, list):
            return False
        hashedPass = result.get('hashed_password')
        verified = result.get('verified')
        if bcrypt.checkpw(request.form.get('password', '').encode('utf-8'), hashedPass.encode('utf-8')) and verified:
            return True
        return False

    def getId(self, request):
        """
        Retrieves the user ID associated with the current session.

        Args:
            request: The request object.

        Returns:
            str or None: User ID if found, None otherwise.
        """
        session = request.cookies.get('session')
        return AuthenticationHandler.__sessions.get(session)

    def tokenGenerator(self):
        return secrets.token_urlsafe(69)


authenticate = AuthenticationHandler()
