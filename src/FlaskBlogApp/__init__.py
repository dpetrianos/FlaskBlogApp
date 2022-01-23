from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from datetime import timedelta
from flask_login import LoginManager

app = Flask(__name__)

# Τα sessions απαιτουν να έχουμε δώσει τιμή στο SECRET_KEY
app.config["SECRET_KEY"] = 'b668cbc68d29fd2b7f5976c54c39f6ec'
app.config['WTF_CSRF_SECRET_KEY'] = 'fe9d487ba2c9a1f13a5d72fa0d76d3fb'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_course_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=10)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=10)

db =  SQLAlchemy(app)   # connects our app with sqlalchemy db 

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"
login_manager.login_message = "Παρακαλόύμε κάντε login για να μπορέσετε να δείτε αυτή τη σελίδα."

from FlaskBlogApp import routes, models
