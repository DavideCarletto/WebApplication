import flask_login
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_required, login_user
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import db_handler
from Models import User

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

profile_img_path = "images/user.jpg"

@app.route("/")
def login_page():

    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    psd = request.form.get("password")

    user = db_handler.get_user_by_username_psd(username, psd)

    if user is not None:
        new = User (id = user["id"], username=user["username"], psd=user["password"], profile_img_path=user["profile_img_path"])
        login_user(new, True)
    else:
        print("Errore nell'autenticazione: utente non valido.")

    return redirect(url_for("index"))

@app.route('/home')
@login_required
def index():  # put application's code here
    posts = db_handler.get_posts()
    style = url_for('static', filename="css/style.css")
    return render_template("index.html", style=style, posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = db_handler.get_single_post(id)
    comments = db_handler.get_comments_from_post(id)
    post["comment_list"] = comments
    style = url_for('static', filename="css/style2.css")
    return render_template("post.html", style=style, post=post)


@app.route('/info')
def about():
    style = url_for('static', filename="css/style.css")
    return render_template("info.html", style=style)


@app.route('/', methods=["POST"])
def create_post():
    try:
        username = request.form.get("username")

        testo = request.form.get("testo")

        if len(testo) < 30 or len(testo) > 200:
            raise Exception

        post_img = request.files["post_img"]
        filename = secure_filename(post_img.filename)
        post_img.save(f"static/images/{filename}")

        data = request.form.get("inputDate")
        data_datetime = datetime.strptime(data, "%Y-%m-%d")

        current_date = datetime.now()

        if data_datetime < current_date:
            raise Exception

        id = db_handler.get_last_post_id()

        if id == None:
            id = (0,)

        new_post = {"id": id[0]+1,"username": f"{username}", "data": f"{data}", "testo": f"{testo}", "post_img_path": f"images/{filename}"}

        db_handler.insert_post(new_post)
        flash("Creazione post eseguita con successo!", "success")

    except Exception:
        flash("Qualcosa è andato storto nella creazione del post, riprovare.", "danger")

    return redirect(url_for('index'))
@app.route('/post/<int:id>', methods=["POST"])
def add_comment(id):
    try:
        username = request.form.get("username")
        rate = int(request.form.get("rate"))
        comment = request.form.get("comment")

        if len(username) == 1:
            username = "@Anonimo"

        if len(comment) == 0:
            raise Exception

        comment_id = db_handler.get_last_comment_id()

        if comment_id == None:
            comment_id = (0,)

        new_comment = {"id": comment_id[0]+1, "username": f"{username}", "data": f"{datetime.now().date()}", "testo": f"{comment}", "rate":f"{rate}","profile_img_path": f"{profile_img_path}"}

        db_handler.insert_comment(id, new_comment)
        flash("Commento aggiunto con successo!", "success")

    except Exception:
        flash("Errore nella creazione del commento", "danger")

    return redirect(url_for("post", id = id))

@login_manager.user_loader
def load_user(user_id):

    db_user = db_handler.get_user_by_id(user_id)
    if db_user is not None:
        user = User(id=db_user['id'], username=db_user['username'],	psd= db_user['password'], profile_img_path=db_user['profile_img_path'])
    else:
        user = None

    return user


if __name__ == '__main__':
    app.run()
