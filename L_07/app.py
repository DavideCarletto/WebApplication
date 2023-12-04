from flask import Flask, render_template, url_for, request, redirect, flash
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.urandom(24)

testo = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus quaerat voluptates, eveniet molestias architecto minima explicabo animi deleniti repudiandae natus, possimus porro reiciendis vel obcaecati ab ullam dolorum quas. Aut! "
profile_img_path = "images/user.jpg"
post_img_path_1 = "images/img1.jpg"
post_img_path_2 = "images/img2.jpg"
post_img_path_3 = "images/img3.jpg"
posts = [{"username": "@Alberto", "data": "2 giorni fa", "testo": f"{testo}", "profile_img": f"{profile_img_path}",
          "post_img": f"{post_img_path_1}"},
         {"username": "@Luigi", "data": "2 giorni fa", "testo": f"{testo}", "profile_img": f"{profile_img_path}",
          "post_img": f"{post_img_path_2}"},
         {"username": "@Juan", "data": "1 settimana fa", "testo": f"{testo}", "profile_img": f"{profile_img_path}",
          "post_img": f"{post_img_path_3}"}
         ]


@app.route('/')
def index():  # put application's code here
    style = url_for('static', filename="css/style.css")
    return render_template("index.html", style=style, posts=posts)


@app.route('/post/<int:id>')
def post(id):
    post = posts[id - 1]
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

        new_post = {"username": f"{username}", "data": f"{data}", "testo": f"{testo}",
                    "profile_img": f"{profile_img_path}", "post_img": f"images/{filename}"}
        posts.append(new_post)
        flash("Creazione post eseguita con successo!", "success")

    except Exception:
        flash("Qualcosa è andato storto nella creazione del post, riprovare.", "danger")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
