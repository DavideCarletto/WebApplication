import sqlite3

foto_column_names= ["id", "percorsoFoto", "main"]
def get_foto_from_annuncio(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT FotoID, PercorsoFoto, Main FROM Foto WHERE IDAnnuncio= ?"

    fotopath = cursor.execute(sql, (id,)).fetchall()
    fotopath = [dict(zip(foto_column_names, foto)) for foto in fotopath]
    cursor.close()
    conn.close()

    return fotopath

def get_main_foto_from_annuncio(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT PercorsoFoto FROM Foto WHERE IDAnnuncio = ? AND Main = 'SI'"
    mainfotopath = cursor.execute(sql, (id,)).fetchone()[0]

    cursor.close()
    conn.close()

    return mainfotopath

def insert_photo_in_annuncio(id_annuncio, percorso, main="NO"):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "INSERT INTO Foto (PercorsoFoto, IDAnnuncio, Main) VALUES (?,?,?)"

    cursor.execute(sql, (percorso, id_annuncio, main))
    conn.commit()

    cursor.close()
    conn.close()

def get_id_annuncio_from_foto(id_foto):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT IDAnnuncio FROM Foto WHERE FotoID = ?"

    id_annuncio = cursor.execute(sql, (id_foto,)).fetchone()[0]

    cursor.close()
    conn.close()

    return id_annuncio

def delete_foto(id_foto):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "DELETE FROM Foto WHERE FotoID = ?"

    cursor.execute(sql, (id_foto,))

    conn.commit()

    cursor.close()
    conn.close()

    return

def set_main(id_foto):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "UPDATE Foto SET Main = 'SI' WHERE FotoID = ?"

    cursor.execute(sql, (id_foto,))
    conn.commit()

    cursor.close()
    conn.close()
