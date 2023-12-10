from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import db_handler

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.urandom(24)

profile_img_path = "images/user.jpg"

@app.route('/')
def index():  # put application's code here
    posts = db_handler.get_posts()

    style = url_for('static', filename="css/style.css")
    return render_template("index.html", style=style, posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = db_handler.get_single_post(id)
    comments = db_handler.get_comments_from_post(id)

    post["comment_list"] = comments
    print(post)
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

        new_post = {"id": id[0]+1,"username": f"{username}", "data": f"{data}", "testo": f"{testo}",
                    "profile_img_path": f"{profile_img_path}", "post_img_path": f"images/{filename}"}

        db_handler.insert_post(new_post)
        flash("Creazione post eseguita con successo!", "success")

    except Exception:
        flash("Qualcosa è andato storto nella creazione del post, riprovare.", "danger")

    return redirect(url_for('index'))
@app.route('/post/<int:id>', methods=["POST"])
def add_comment(id):
    try:
        username = "@"+request.form.get("username")
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

if __name__ == '__main__':
    app.run()
