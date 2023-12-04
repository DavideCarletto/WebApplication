from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

testo = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ducimus quaerat voluptates, eveniet molestias architecto minima explicabo animi deleniti repudiandae natus, possimus porro reiciendis vel obcaecati ab ullam dolorum quas. Aut! "
profile_img_path = "images/user.jpg"
post_img_path_1 = "images/img1.jpg"
post_img_path_2 = "images/img2.jpg"
post_img_path_3 = "images/img3.jpg"
@app.route('/')
def index():  # put application's code here
    posts = [{"username":"@Alberto", "data":"2 giorni fa", "testo":f"{testo}", "profile_img":f"{profile_img_path}", "post_img": f"{post_img_path_1}"},
             {"username":"@Luigi", "data":"2 giorni fa", "testo":f"{testo}", "profile_img":f"{profile_img_path}", "post_img": f"{post_img_path_2}"},
             {"username":"@Juan", "data":"1 settimana fa", "testo":f"{testo}", "profile_img":f"{profile_img_path}","post_img": f"{post_img_path_3}"}
             ]
    post = url_for('post')
    info = url_for('info')
    style = url_for('static', filename="css/style.css")
    return render_template("index.html", post = post, style = style,  info = info, posts = posts)

@app.route('/post')
def post():
    info = url_for('info')
    style = url_for('static', filename = "css/style2.css")
    return render_template("post.html", style = style, info = info)

@app.route('/info')
def info():
    index = url_for('index')
    style = url_for('static',filename = "css/info.css")
    return render_template("info.html", index = index, style = style)

if __name__ == '__main__':
    app.run()
