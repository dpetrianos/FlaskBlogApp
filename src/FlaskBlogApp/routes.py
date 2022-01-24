from cmath import log
from flask import (render_template,
                   redirect,
                   url_for,
                   request,
                   flash, abort,
                   session)   # session 

from FlaskBlogApp.forms import SignupForm, LoginForm, NewArticleForm, AccountUpdateForm

from FlaskBlogApp import app, db, bcrypt

from FlaskBlogApp.models import User, Article 

from flask_login import login_user, current_user, logout_user, login_required

import secrets, os 

from PIL import Image

# Το size είναι ένα tuple της μορφής (640,480)
def image_save(image, where, size):
    random_filename = secrets.token_hex(12)
    file_name, file_extension = os.path.splitext(image.filename)
    image_filename = random_filename + file_extension
    
    # where = 'profiles_images'
    image_path = os.path.join(app.root_path , 'static/images/', where,  image_filename)

    img = Image.open(image)

    img.thumbnail(size)
    img.save(image_path)

    return image_filename


@app.route("/index/")
@app.route("/")
def root(): 

    # user = None
    # if "user" in session:
    #     user = session["user"]

    articles = Article.query.order_by(Article.date_created.desc()).paginate(per_page=5, page=1)
    # articles = Article.query.all()
    # return render_template("index.html", articles=articles, myuser=user)    #session
    return render_template("index.html", articles=articles)



@app.route("/articles_by_author/<int:author_id>")
def articles_by_author(author_id):

    user = User.query.get_or_404(author_id)
    articles = Article.query.filter_by(author=user).order_by(Article.date_created.desc())

    return render_template("articles_by_author.html", articles=articles, author=user)


@app.route("/signup/", methods=["GET", "POST"])
def signup():

    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data

        encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8') 

        user = User(username=username, email=email, password=encrypted_password)
        db.session.add(user)
        db.session.commit()

        flash(f"Ο λογαριασμός για τον χρήστη <b> {username} </b> δημιουργήθηκε με επιτυχία", "success")
        # print(username, email, password, password2)
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)




@app.route("/login/", methods=["GET", "POST"])
def login():

    # session.permanent = True

    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            flash(f"Η είσοδος του χρήστη με email: {email} στη σελίδα μας έγινε με επιτυχία.", "success")
            login_user(user, remember=form.remember_me.data)

            next_link = request.args.get("next")

            return redirect(next_link) if next_link else redirect(url_for('root'))
        else:
            flash(f"Η είσοδος του χρήστη ήταν ανεπιτυχής, παρακαλούμε δοκιμάστε ξανά με τα σωστά email/password.", "warning")
        # user = User.query.filter_by(email=email).first()    #session

        # print(email, password)
        # if user and bcrypt.check_password_hash(user.password, password):
        #     # session["user"] = user.username   
        #     session["user"] = { "username": user.username,
        #                         "email": user.email,
        #                         "profile_image": user.profile_image,
        #                         "id": user.id
        #                         }       # if we want to save whole user elements we use dictionary 

        #     flash(f"Η είσοδος του χρήστη με email: {user.email} στη σελίδα μας έγινε με επιτυχία.", "success")
        #     return redirect(url_for('root'))
        # else:
        #     flash(f"Η σύνδεση του χρήστη απέτυχε.", "warning")

    return render_template("login.html", form=form)




@app.route("/logout/")
def logout():
    # session.pop("user",None)
    logout_user()

    flash("Έγινε αποσύνδεση του χρήστη.","success")
    return redirect(url_for("root"))




@app.route("/new_article/", methods=["GET", "POST"])
@login_required
def new_article():
    
    # if "user" in session:
    form = NewArticleForm()

    if request.method == 'POST' and form.validate_on_submit():
        article_title = form.article_title.data
        article_body = form.article_body.data

        # print(article_title, article_body)
        # article = Article(article_title=article_title, article_body=article_body, user_id=current_user.id)
        if form.article_image.data:
            try:
                image_file =  image_save(form.article_image.data, 'articles_images', (640,360))
            except:
                abort(415)  # 418 The server is a  teapot not coffee machine
            article = Article(article_title=article_title, 
                              article_body=article_body, 
                              author=current_user,
                              article_image=image_file)
        else:
            article = Article(article_title=article_title, article_body=article_body, author=current_user)
       
        db.session.add(article)
        db.session.commit()
        flash(f"Το άρθρο με τίτλο <b>{article.article_title}</b> δημιουργήθηκε με επιτυχία","success")

        return redirect(url_for('root'))

    return render_template("new_article.html", form=form, page_title="Εισαγωγή Νέου Άρθρου")
    # else:
    #     flash("Για να δείτε αυτή τη σελίδα θα πρέπει πρώτα να κάνετε l;ogin.", "warning")
    
    

@app.route("/full_article/<int:article_id>", methods=["GET"])
def full_article(article_id):
    article = Article.query.get_or_404(article_id)

    return render_template("full_article.html", article=article)


@app.route("/delete_article/<int:article_id>", methods=["GET","POST"])
@login_required
def delete_article(article_id):
    # article = Article.query.get_or_404(article_id)
    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    if article:
        db.session.delete(article)
        db.session.commit()

        flash(f"Το άρθρο διεγράφη με επιτυχία.","success")
    else:
        flash(f"Το άρθρο δεν βρέθηκε.","warning")
    return redirect(url_for('root'))


@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm(username=current_user.username, email=current_user.email)
    # form.username.data = current_user.username
    # form.email.data = current_user.email

    if request.method == 'POST' and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        #  image_save(image, where, size)

        if form.profile_image.data:
            try:
                image_file =  image_save(form.profile_image.data, 'profiles_images', (150,150))
            except:
                abort(415)  # 418 The server is a  teapot not coffee machine
            current_user.profile_image = image_file

        db.session.commit()

        flash(f"Ο λογαριασμός του χρήστη <b> { current_user.username } </b> ενημερώθηκε με επιτυχία", "success")

        return redirect(url_for('root'))    

    return render_template("account_update.html",form=form)


@app.route("/edit_article/<int:article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):

    article = Article.query.filter_by(id=article_id, author=current_user).first_or_404()

    # if article:
    #     if article.author != current_user:
    #         abort(403)

    form = NewArticleForm(article_title=article.article_title, article_body=article.article_body)
    # form.article_title.data = article.article_title
    # form.article_body.data = article.article_body
    
    if request.method == 'POST' and form.validate_on_submit():
        article.article_title = form.article_title.data
        article.article_body = form.article_body.data

        if form.article_image.data:
            try:
                image_file =  image_save(form.article_image.data, 'articles_images', (640,360))
            except:
                abort(415)  # 418 The server is a  teapot not coffee machine
            
            article.article_image = image_file

        db.session.commit()

        flash(f"Το άρθρο με τίτλο <b> { article.article_title } </b> ενημερώθηκε με επιτυχία", "success")

        return redirect(url_for('root'))   

    return render_template("new_article.html", form=form, page_title="Επεξεργασία Άρθρου") 

