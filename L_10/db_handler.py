import sqlite3

posts_column_names = ("id", "username", "profile_img_path", "data", "testo", "post_img_path", )
comments_column_names = ("id", "username", "data", "testo", "profile_img_path")
usernames_column_names = ("id", "username", "password", "profile_img_path")
def get_posts():

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT P.id, U.username, U.profile_img_path, P.data, P.testo, P.post_img_path FROM Posts P, Utenti U WHERE P.id_utente = U.id"
    cursor.execute(sql)
    posts = cursor.fetchall()

    posts = [dict(zip(posts_column_names, post)) for post in posts]

    for post in posts:
        sql = "SELECT id, id_utente, data, testo FROM Commenti WHERE id_post = ?"
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

    sql = "SELECT id FROM Utenti WHERE username = ?"
    cursor.execute(sql, (post["username"],))
    id_utente = cursor.fetchone()[0]
    sql = "INSERT INTO Posts (id, id_utente, Data, Testo, post_img_path) VALUES (?, ?, ?, ?, ?)"

    cursor.execute(sql, (post["id"], id_utente, post["data"], post["testo"], post["post_img_path"]))
    conn.commit()

    cursor.close()
    conn.close()

    return

def get_single_post(id):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT P.id, U.username, U.profile_img_path, P.data, P.testo, P.post_img_path FROM Posts P, Utenti U WHERE P.id_utente = U.id AND P.id = ?"
    cursor.execute(sql, (id,))

    post = cursor.fetchone()
    post = dict(zip(posts_column_names, post))

    return post
def insert_comment(id_post, comment):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    print(comment["username"])
    sql = "SELECT id FROM Utenti WHERE username = ?"
    cursor.execute(sql, (comment["username"],))
    id_utente = cursor.fetchone()[0]

    sql = "INSERT INTO Commenti (id, id_utente, data, testo, id_post) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (comment["id"], id_utente, comment["data"], comment["testo"], id_post))

    conn.commit()

    cursor.close()
    conn.close()

    return

def get_comments_from_post(id_post):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT C.id, U.username, C.data, C.testo, U.profile_img_path FROM Commenti C, Utenti U WHERE id_utente = U.id AND id_post = ?"
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

def get_user_by_username_psd(username, password):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Utenti where username = ? AND password = ? "

    cursor.execute(sql, (username, password))

    user = cursor.fetchone()

    if user is not None:
        user = dict(zip(usernames_column_names, user))

    cursor.close()
    conn.close()

    return user

def get_user_by_id(id):

    conn = sqlite3.connect("db/posts.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Utenti WHERE id = ?"

    cursor.execute(sql , (id,))

    user = cursor.fetchone()

    if user is not None:
            user = dict(zip(usernames_column_names, user))

    cursor.close()
    conn.close()

    return user