"""

"""
from flask import (
    Flask,
    render_template,
    request, redirect,
    url_for,
    make_response,
    abort,
    jsonify,
    send_from_directory
)
from authentication import authenticate
from authentication import verification
from authentication import reset_handler
from authentication import registration
from authentication import file_handler
from authentication import capsule_handler
from session import session_manager
from authentication import utility
from mail import esmtp
from datetime import datetime
from error import error


app = Flask(__name__)


@app.before_request
def clear_errors():
    # this simple idea saved me from going into a rabit hole
    error.clear_errors()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        token = utility.url_token_generator()

        if registration.register_user(request, token):
            email = request.form.get('email', '').lower().strip()
            username = request.form.get('username', '').strip()
            esmtp.verifyEmail(email, username, token)
            return render_template('emailConfirm.html')
        else:
            return render_template("signup.html", errors=error.errors)

    return render_template("signup.html")


@app.route('/dashboard')
def dashboard():
    if not session_manager.is_authenticated(request):
        return redirect(url_for('login'))

    return render_template('dashboard.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session = authenticate.login_user(request)
        if session:
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session', session, max_age=3600)
            return response
        else:
            return render_template("login.html", error='Check email/password')

    return render_template("login.html")


@app.route('/logout')
def logout():
    session = request.cookies.get('session', '')
    session_manager.delete_session(session)
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', max_age=0)
    return response


@app.route('/confirm/<token>')
def emailConfirm(token):
    verification.validate_email(token)
    return redirect(url_for('login'))


@app.route('/forgotpassword', methods=['POST', 'GET'])
def forgotPassword():
    if request.method == 'POST':
        # generate the token and send an email
        email = request.form.get('email', '').lower().strip()
        if verification.email_exists(email):
            url_token = utility.url_token_generator()
            reset_handler.set_password_reset_token(email, url_token)
            esmtp.sendResetPass(email, url_token)
        return render_template('passresetconfirm.html')
    return render_template('forgotpass.html')


@app.route('/reset/<token>', methods=['POST', 'GET'])
def resetPassword(token):
    if request.method == 'POST':
        if reset_handler.change_password(request, token):
            return redirect(url_for('login'))
        return render_template('resetpassword.html', errors='No user Found please check your link')
    return render_template('resetpassword.html')


@app.route('/api/v1/capsules/', methods=['GET'])
def capsules():
    if not session_manager.is_authenticated(request):
        return jsonify({'error': 'User not authenticated'}), 401

    succes, capsules = capsule_handler.get_capsules(request)

    if not succes:
        return jsonify({'error': error.errors}), 401

    if not capsules:
        return jsonify({'error': 'No capsule available for this user'}), 401

    for capsule in capsules:
        domain = 'https://www.orino.tech/capsule/share/'
        capsulid = capsule['capsuleid']
        link = capsule['link']
        if not link:
            token = utility.url_token_generator()
            capsule_handler.create_link_for_a_capsule(token, capsulid)
            capsule['link'] = domain + token
        else:
            capsule['link'] = domain + link

    return jsonify(capsules)


@app.route('/api/v1/capsules/add', methods=['POST'])
def addcapsule():
    if not session_manager.is_authenticated(request):
        return jsonify({'error': 'User not authenticated'}), 401

    title = request.form.get('title', '').strip()
    image = request.files.get('image')
    message = request.form.get('message', '').strip()
    open_at = request.form.get('open_at')

    if not open_at:
        return jsonify({'error': 'open_at missing'}), 400

    if not title:
        return jsonify({'error': 'title is missing'}), 400

    if not message:
        return jsonify({'error': 'message is missing'}), 400

    try:
        open_at = datetime.strptime(open_at, '%Y-%m-%d').date()
    except:
        return jsonify({'error': 'open_at isnt valid'}), 400

    currentDate = datetime.utcnow().date()

    if open_at <= currentDate:
        return jsonify({'error': 'open_at isnt valid'}), 400

    if image:
        filename = image.filename
        maxsize = 10 * 1024 * 1024
        if image.content_length > maxsize:
            return jsonify({'error': 'image size exceeds the limit'}), 400
        if not file_handler.is_allowed_file(filename):
            return jsonify({'error': 'image not allowed'}), 400

    capsule_handler.add_capsule_to_db(request, title, image, message, open_at)

    return jsonify({'success': True}), 200


@app.route('/js/<filename>')
def serve_js(filename):
    # this will be removed as nginx will handle scripts
    return send_from_directory('js/', filename)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
