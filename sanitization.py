"""
Sanitization Module

This module defines a simple Sanitization class for validating login and
registration forms.

Usage:
-----------
Instantiate the Sanitization class and use its methods to validate user
input from forms.

Example:
-----------
from sanization_module import Sanitization

# Instantiate the Sanitization class
sanitize = Sanitization()

# Validate login form
login_errors = sanitize.loginForm(request)

# Validate registration form
registration_errors = sanitize.registrationForm(request)
"""


import bcrypt
import re


class Sanitization:
    """
    Simple Sanitization Class
    """

    def loginForm(self, request):
        """
        Validates login form input.

        Parameters:
        -----------
        request : Flask request object
            The request object containing form data.

        Returns:
        -----------
        errors : list
            List of error messages indicating issues with the form input.
        """
        errors = []
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        # both patterns are not mine
        emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_+{}|:\'<>,.?/~`]{8,30}$'
        if email == '':
            errors.append('Invalid Email.')
        elif not re.match(emailPattern, email):
            errors.append('Invalid Email.')
        if password == '':
            errors.append('Invalid Password.')
        elif not re.match(passwordPattern, password):
            errors.append('Invalid Password.')
        return errors

    def registrationForm(self, request):
        """
        Validates registration form input.

        Parameters:
        -----------
        request : Flask request object
            The request object containing form data.

        Returns:
        -----------
        errors : list
            List of error messages indicating issues with the form input.
        """
        errors = []
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('cpassword', '').strip()
        # both patterns are not mine
        emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_+{}|:\'<>,.?/~`]{8,30}$'
        if username == '' or len(username) > 35 or len(username) < 3:
            errors.append('Invalid username.')
        if email == '':
            errors.append('Invalid Email.')
        elif not re.match(emailPattern, email):
            errors.append('Invalid Email.')
        if password == '' or confirm_password == '' or password != confirm_password:
            errors.append('Invalid Password.')
        elif not re.match(passwordPattern, password):
            errors.append('Invalid Password.')
        return errors


sanitize = Sanitization()
