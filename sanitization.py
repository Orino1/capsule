
import bcrypt
import re
from error import error

class Sanitization:

    def reset_password_form(self, request):
        password = request.form.get('password1', '').strip()
        confirm_password = request.form.get('password2', '').strip()
        # both patterns are not mine
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_+{}|:\'<>,.?/~`]{8,30}$'

        if password == '' or confirm_password == '' or password != confirm_password:
            error.add_error('Invalid Password')
        elif not re.match(passwordPattern, password):
            error.add_error('Invalid Password')

        if error.errors:
            return False

        return True

    def login_form(self, request):

        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        # both patterns are not mine
        emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_+{}|:\'<>,.?/~`]{8,30}$'
        if email == '':
            error.add_error('Invalid Email.')
        elif not re.match(emailPattern, email):
            error.add_error('Invalid Email.')

        if password == '':
            error.add_error('Invalid Password.')
            return False
        elif not re.match(passwordPattern, password):
            error.add_error('Invalid Password.')

        if error.errors:
            return False

        return True

    def registration_form(self, request):
 
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('cpassword', '').strip()
        # both patterns are not mine
        emailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        passwordPattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:\'<>,.?/~`])[A-Za-z\d!@#$%^&*()_+{}|:\'<>,.?/~`]{8,30}$'

        if username == '' or len(username) > 35 or len(username) < 3:
            error.add_error('Invalid username.')

        if email == '':
            error.add_error('Invalid Email.')
        elif not re.match(emailPattern, email):
            error.add_error('Invalid Email.')

        if password == '' or confirm_password == '' or password != confirm_password:
            error.add_error('Invalid Password.')
        elif not re.match(passwordPattern, password):
            error.add_error('Invalid Password.')

        if error.errors:
            return False

        return True


sanitize = Sanitization()
