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
import os
from error import error

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
            query = 'UPDATE users SET verified = 1 WHERE email_verification_token = %s'
            param = (token,)
            db.insert(query, param)

    def setPassResetToken(self, email, token):
        query = "UPDATE users SET reset_password_token = %s WHERE email = %s"
        param = (token, email)
        db.insert(query, param)

    def changePass(self, request, token):
        if not sanitize.resetPassForm(request):
            return False

        if not db.resetTokenExists(token):
            return False

        password = request.form.get('password1', '').strip()
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        query = "UPDATE users SET hashed_password = %s WHERE reset_password_token = %s"
        param = (hashedPassword, token)
        db.insert(query, param)
        query = "UPDATE users SET reset_password_token = NULL WHERE reset_password_token = %s"
        param = (token,)
        return db.insert(query, param)


    def registerUser(self, request, token):
        """
        registerUser(request)

        Registers a new user based on the provided registration form.

        Args:
            request: The request object containing user registration details.

        Returns:
            list of errors or empty list: List of errors if registration fails, empty list otherwise.
        """
        if not sanitize.registrationForm(request):
            return False

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

        if db.emailExists(email):
            return False, 'This email already exists'

        query = f"INSERT INTO users (id, username, email, hashed_password, email_verification_token) VALUES (%s, %s, %s, %s, %s)"
        return db.insert(query, data)

    def loginUser(self, request):
        """
        Logs in a user based on the provided login form.

        Args:
            request: The request object containing user login details.

        Returns:
            str or list of errors: Session token if login is successful, list of errors otherwise.
        """
        if not sanitize.loginForm(request):
            return False

        query = f'SELECT hashed_password, verified FROM users WHERE email = %s'
        param = (request.form.get('email', '').lower(),)

        succes, result = db.queryOne(query, param)

        if not succes and not result:
            return False

        hashedPass = result.get('hashed_password')
        verified = result.get('verified')

        if bcrypt.checkpw(request.form.get('password', '').encode('utf-8'), hashedPass.encode('utf-8')) and verified:
            query = f'SELECT id FROM {AuthenticationHandler.__usersTable} where email = %s'
            param = (request.form.get('email'.lower()),)
            result = db.queryOne(query, param)
            session = self.genSessions()
            self.__sessions[session] = result['id']
            return session
        
        return False

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
        if AuthenticationHandler.__sessions.get(session):
            return True
        return False

    def getId(request):
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
    
    def allowedFile(self, filename):
        allowerExtention = {'png', 'jpg', 'jpeg', 'gif'}
        extention = filename.split('.')[-1]
        return extention in allowerExtention

    def addCapsuleToDB(self, request, title, image, message, open_at):
        # Remember we gona change the whole classes to return true or false and no longer returning the list with errors in it
        capsuleId = str(uuid.uuid4())
        userId = AuthenticationHandler.getId(request)
        
        if image:
            extention = image.filename.split('.')[-1]
            imagename = f"{capsuleId}.{extention}"
            imagePath = f"images/{imagename}"
            image.save(imagePath)
            query = "INSERT INTO capsules (capsuleid, title, user_id, image, message, open_at) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (capsuleId, title, userId, imagePath, message, open_at)
        else:
            query = "INSERT INTO capsules (capsuleid, title, user_id, message, open_at) VALUES (%s, %s, %s, %s, %s)"
            params = (capsuleId, title, userId, message, open_at)

        return db.insert(query, params)


    def getcapsules(self , request):
        userid = AuthenticationHandler.getId(request)
        query = 'SELECT capsuleid, title, image, message, link FROM capsules WHERE user_id = %s AND opened = TRUE'
        param = (userid,)
        return db.queryAll(query, param)

    def create_link_for_a_capsule(self, capsulid):
        link = self.tokenGenerator()
        query = 'UPDATE capsules SET link = %s WHERE  capsuleid = %s'
        param = (link, capsulid)
        db.insert(query, param)
        return link

authenticate = AuthenticationHandler()
