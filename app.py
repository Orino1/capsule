"""

"""
from flask import (
    Flask,
    render_template,
    request, redirect,
    url_for
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


@app.route("/login")
def dashboard():
    """
    for testing
    """
    return 'ok'


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
