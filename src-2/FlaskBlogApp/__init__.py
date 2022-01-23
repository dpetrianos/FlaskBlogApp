from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = 'my_secret'
app.config['WTF_CSRF_SECRET_KEY'] = '9f8a1aaa0022e95f3ed1b1a93f8916f5'

from FlaskBlogApp import routes
