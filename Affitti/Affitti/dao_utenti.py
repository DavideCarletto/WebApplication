import sqlite3

user_column_names = ("UserID", "Email", "Password", "Username", "Type")

def get_user_from_email(email):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Utente WHERE Email = ?"
    cursor.execute(sql, (email, ))

    user = cursor.fetchone()

    if user is not None:
        user = dict(zip(user_column_names, user))

    cursor.close()
    conn.close()

    return user
def insert_user(user):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "INSERT INTO UTENTE (Email, Password, Username, Type) VALUES (?,?,?,?)"
    success = False

    try:
        cursor.execute(sql, (user["email"], user["password"], user["username"], user["type"]))
        conn.commit()
        success=True

    except Exception as e:
        print("Error", e)
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_email_from_id(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT Email FROM UTENTE WHERE UserID = ?"

    user = cursor.execute(sql, (id,)).fetchone()[0]

    cursor.close()
    conn.close()

    return user

def get_user_from_id(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM UTENTE WHERE UserID = ?"
    user = cursor.execute(sql, (id,)).fetchone()

    user = dict(zip(user_column_names, user)) if user is not None else None

    cursor.close()
    conn.close()

    return user
