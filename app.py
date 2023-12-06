"""

"""
from flask import (
    Flask,
    render_template,
    request, redirect,
    url_for,
    make_response
)
from authentication import authenticate


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
        errors = authenticate.registerUser(request)
        if errors == []:
            return redirect(url_for('login'))
        else:
            return render_template("signup.html", errors=errors)

    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    """
    for testing
    """
    return 'ok'


@app.route("/login", methods=['POST', 'GET'])
def login():
    """
    Handle user login.

    If user is authenticated, redirect to the dashboard page.
    If the request method is POST, attempt to log in the user.
    """
    if authenticate.isAuthenticated(request):
        return redirect(url_for('profile'))

    if request.method == 'POST':
        errors = authenticate.loginUser(request)
        if not isinstance(errors, list):
            session = errors
            response = make_response(redirect(url_for('profile')))
            response.set_cookie('session', session, max_age=3600)
            return response
        else:
            return render_template("login.html", errors=errors)

    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
