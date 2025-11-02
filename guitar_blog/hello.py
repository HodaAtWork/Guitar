#
# Tutorial https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3
#
# STEP 2 base application
#


from flask import Flask

app = Flask(__name__)  # a Flask application instance. __name__ holds name current Python module

@app.route('/')  # a decorator on main url '/': function's return value => http response to display by http client like a webbrowser

def hello():
    return 'Hello, world!'
