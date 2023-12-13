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
from mail import esmtp
from datetime import datetime
import base64

app = Flask(__name__)


@app.route("/")
def home():
    """
    Render the home page.
    """
    return render_template("home.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    """
    Handle user signup.

    If user is authenticated, redirect to the dashboard page.
    If the request method is POST, attempt to register the user.
    """
    if authenticate.isAuthenticated(request):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        token = authenticate.tokenGenerator()
        errors = authenticate.registerUser(request, token)
        if errors == []:
            email = request.form.get('email', '').lower().strip()
            username = request.form.get('username', '').strip()
            esmtp.verifyEmail(email, username, token)
            return render_template('emailConfirm.html')
        else:
            return render_template("signup.html", errors=errors)

    return render_template("signup.html")


@app.route('/dashboard')
def dashboard():
    """
    Render the user dashboard.
    Redirect to login if the user is not authenticated.
    """
    if not authenticate.isAuthenticated(request):
        return redirect(url_for('login'))


    return render_template('dashboard.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    """
    Handle user login.

    If user is authenticated, redirect to the dashboard page.
    If the request method is POST, attempt to log in the user.
    """
    if authenticate.isAuthenticated(request):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        errors = authenticate.loginUser(request)
        if not isinstance(errors, list):
            session = errors
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session', session, max_age=3600)
            return response
        else:
            return render_template("login.html", errors=errors)

    return render_template("login.html")


@app.route('/logout')
def logout():
    """
    Handle user logout.

    Delete the user session and redirect to the login page.
    """
    session = request.cookies.get('session', '')
    authenticate.deleteSession(session)
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', max_age=0)
    return response


@app.route('/confirm/<token>')
def emailConfirm(token):
    """

    """
    authenticate.validateEmail(token)
    return redirect(url_for('login'))

@app.route('/forgotpassword', methods=['POST', 'GET'])
def forgotPassword():
    """
    """
    if request.method == 'POST':
        # generate the token and send an email
        email = request.form.get('email', '').lower().strip()
        if authenticate.email(email):
            token = authenticate.tokenGenerator()
            authenticate.setPassResetToken(email, token)
            esmtp.sendResetPass(email, token)
        return render_template('passresetconfirm.html')
    return render_template('forgotpass.html')

@app.route('/reset/<token>', methods=['POST', 'GET'])
def resetPassword(token):
    #resetPass
    if request.method == 'POST':
        errors = authenticate.changePass(request, token)
        if errors == []:
            return redirect(url_for('login'))
        return render_template('resetpassword.html', errors=errors)
    return render_template('resetpassword.html')

@app.route('/api/v1/capsules/', methods=['GET'])
def capsules():
    if not authenticate.isAuthenticated(request):
        return jsonify({'error': 'User not authenticated'}), 401

    capsules = authenticate.getcapsules(request)

    if not capsules:
        return jsonify({'error': 'No capsule available for this user'}), 401

    for capsule in capsules:
        domain = 'https://www.orino.tech/capsule/share/'
        capsulid = capsule['capsuleid']
        link = capsule['link']
        
        if not link:
            token = authenticate.create_link_for_a_capsule(capsulid)
            capsule['link'] = domain + token
        else:
            capsule['link'] = domain + link

    return jsonify(capsules)

@app.route('/api/v1/capsules/add', methods=['POST'])
def addcapsule():
    if not authenticate.isAuthenticated(request):
        return jsonify({'error': 'User not authenticated'}), 401

    if not request.form.get('open_at'):
        return jsonify({'error': 'open_at date missing'}), 400

    title = request.form.get('message', '').strip()
    image = request.files.get('image')
    message = request.form.get('message', '').strip()
    open_at = request.form.get('open_at')
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
        abort(404)

    if image:
        filename = image.filename
        maxsize = 10 * 1024 * 1024
        if image.content_length > maxsize:
            return jsonify({'error': 'image size exceeds the limit'}), 400
        if not authenticate.allowedFile(filename):
            return jsonify({'error': 'image not allowed'}), 400

    authenticate.addCapsuleToDB(request, title, image, message, open_at)

    return jsonify({'success': True}), 200

@app.route('/js/<filename>')
def serve_js(filename):
    # this will be removed as nginx will handle scripts
    return send_from_directory('js/', filename)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
