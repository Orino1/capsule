from flask import Flask, render_template
"""

"""

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
