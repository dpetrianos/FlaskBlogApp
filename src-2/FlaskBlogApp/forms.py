from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
# from wtforms import validators
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    username = StringField(label="Username", 
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    email = StringField(label="email",
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Email(message="Παρακαλώ εισάγετε ένα έγκυρο email")])
    
    password = StringField(label="password",
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες")])
    
    password2 = StringField(label='επιβεβαίωση password',
                 validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=15, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 15 χαρακτήρες"),
                            EqualTo('password', message="Τα δύο password πρέπει να είναι ίδια")])

    submit = SubmitField('Εγγραφή')
 


class LoginForm(FlaskForm):
    email = StringField(label="email",
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Email(message="Παρακαλώ εισάγετε ένα έγκυρο email")])
    
    password = StringField(label="password",
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό.")])
    
    submit = SubmitField('Είσοδος')
 


class NewArticleForm(FlaskForm):
    article_title = StringField(label="Τίτλος Άρθρου", 
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=3, max=50, message="Αυτό το πεδίο πρέπει να είναι από 3 έως 50 χαρακτήρες")])
    
    article_body = TextAreaField(label="Κείμενο Άρθρου",
                validators=[DataRequired(message="Αυτό το πεδίο δεν μπορεί να είναι κενό."),
                            Length(min=5, message="Το κείμενο του άρθρου πρέπει να έχει τουλάχιστον 5 χαρακτήρες")])
    
    submit = SubmitField('Αποστολή')
 