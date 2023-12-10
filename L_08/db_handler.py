import sqlite3

posts_column_names = ("id", "username", "data", "testo", "profile_img_path", "post_img_path")
comments_column_names = ("id", "username", "data", "testo", "profile_img_path")
def get_posts():

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Posts"
    cursor.execute(sql)
    posts = cursor.fetchall()

    posts = [dict(zip(posts_column_names, post)) for post in posts]
    for post in posts:
        if "@" not in post["username"]:
            post["username"] = "@" + post["username"]
        sql = "SELECT id, username, data, testo, profile_img FROM Commenti WHERE id_post = ?"
        comments = cursor.execute(sql, (post["id"],)).fetchall()

        if "comment_list" not in post:
            post["comment_list"] = []

        comments = [dict(zip(comments_column_names, comment)) for comment in comments]
        post["comment_list"] = comments

    cursor.close()
    conn.close()

    return posts

def insert_post(post):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "INSERT INTO Posts (id, Username, Data, Testo, profile_img_path, post_img_path) VALUES (?, ?, ?, ?, ?, ?)"

    cursor.execute(sql, (post["id"], post["username"], post["data"], post["testo"], post["profile_img_path"], post["post_img_path"]))
    conn.commit()

    cursor.close()
    conn.close()

    return

def get_single_post(id):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Posts WHERE id = ?"
    cursor.execute(sql, (id,))

    post = cursor.fetchone()
    post = dict(zip(posts_column_names, post))

    return post
def insert_comment(id_post, comment):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "INSERT INTO Commenti (id, username, data, testo, profile_img, id_post) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, (comment["id"], comment["username"], comment["data"], comment["testo"], comment["profile_img_path"], id_post))

    conn.commit()

    cursor.close()
    conn.close()

    return

def get_comments_from_post(id_post):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT id, username, data, testo, profile_img FROM Commenti WHERE id_post = ?"
    cursor.execute(sql, (id_post,))

    comments = cursor.fetchall()

    comments = [dict(zip(comments_column_names, comment)) for comment in comments]

    cursor.close()
    conn.close()

    return comments
def get_last_post_id():

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT id FROM Posts ORDER BY id DESC LIMIT 1;"

    cursor.execute(sql)

    id = cursor.fetchone()

    cursor.close()
    conn.close()

    return id

def get_last_comment_id():

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT id FROM Commenti ORDER BY id DESC LIMIT 1;"

    cursor.execute(sql, )

    id = cursor.fetchone()

    cursor.close()
    conn.close()

    return id

