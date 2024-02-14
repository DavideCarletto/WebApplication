import os
import sqlite3

from flask_login import current_user
from werkzeug.utils import secure_filename

import dao_foto
import dao_prenotazioni

annuncio_column_names = ("id", "titolo", "indirizzo", "tipo", "locali", "desc", "prezzo", "arredata", "disponibile", "userid")
def get_annunci_disponibili(short_address = False):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM ANNUNCIO WHERE Disponibile = 'SI' "

    annunci = cursor.execute(sql).fetchall()
    annunci_dict = [dict(zip( annuncio_column_names, annuncio)) for annuncio in annunci]
    annunci_dict = get_annunci_good_format(annunci_dict, short_address)

    cursor.close()
    conn.close()

    return annunci_dict

def get_annunci_good_format(annunci, short_address = False):
    for annuncio in annunci:
        if short_address is True:
            città = annuncio["indirizzo"].split(',')
            annuncio["indirizzo"] = città[2].strip()

        mainfotopath = dao_foto.get_main_foto_from_annuncio(int(annuncio["id"]))
        annuncio["fotopath"] = mainfotopath

    return annunci

def get_annuncio_from_id(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Annuncio WHERE AnnuncioID = ?"

    annuncio = dict(zip(annuncio_column_names, cursor.execute(sql, (id,)).fetchone()))

    cursor.close()
    cursor.close()

    return annuncio

def is_prenotabile(id):
    prenotabile = True
    annuncio = get_annuncio_from_id(id)

    if not current_user.is_authenticated or len(dao_prenotazioni.get_richieste_non_rifiutate_annuncio_from_utente(id, current_user.id)) != 0 or annuncio["userid"] == current_user.id:
        prenotabile = False

    return prenotabile



def get_annunci_from_userID(id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Annuncio WHERE UserID = ?"

    annunci = [dict(zip(annuncio_column_names, annuncio)) for annuncio in cursor.execute(sql, (id,)).fetchall()]

    cursor.close()
    conn.close()

    return annunci

def aggiungi_annuncio(annuncio):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "INSERT INTO Annuncio (Titolo, IndirizzoCasa, TipoCasa, NumeroLocali, Descrizione, PrezzoMensile, Arredata, Disponibile, UserID) VALUES (?,?,?,?,?,?,?,?,?)"

    cursor.execute(sql, (annuncio["titolo"],annuncio["indirizzo"], annuncio["tipo"],  annuncio["n_locali"], annuncio["descrizione"],annuncio["prezzo"],annuncio["arredata"],annuncio["disponibile"],current_user.id))

    annuncio_id = cursor.lastrowid
    conn.commit()

    cursor.close()
    conn.close()
    count=0
    first = True
    for img in annuncio["images"]:
        if count < 5:
            filename = secure_filename(img.filename)
            main = "NO" if not first else "SI"

            img.save(os.path.join('static/Images/', filename))

            dao_foto.insert_photo_in_annuncio(annuncio_id, f"Images/{filename}", main)
            count += 1
            first = False
        else:
            break


    return

def delete_annuncio_from_id(annuncio_id):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "DELETE FROM Annuncio WHERE AnnuncioID = ?"

    cursor.execute(sql,  (annuncio_id,))
    conn.commit()

    sql ="DELETE FROM Foto WHERE IDAnnuncio = ?"

    cursor.execute(sql, (annuncio_id,))
    conn.commit()

    cursor.close()
    conn.close()

def modifica_annuncio_from_id(id, titolo, tipo, locali, descrizione, prezzo, arredata, disponibile):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    query = "UPDATE Annuncio SET"
    values = []

    if titolo:
        query += " Titolo = ?,"
        values.append(titolo)
    if tipo:
        query += " TipoCasa = ?,"
        values.append(tipo)
    if locali:
        query += " NumeroLocali = ?,"
        values.append(locali)
    if descrizione:
        query += " Descrizione = ?,"
        values.append(descrizione)
    if prezzo:
        query += " PrezzoMensile = ?,"
        values.append(prezzo)
    if arredata:
        query += " Arredata = ?,"
        values.append(arredata)
    if disponibile:
        query += " Disponibile = ?,"
        values.append(disponibile)

    query = query.rstrip(',')

    query += " WHERE AnnuncioID = ?"
    values.append(id)

    cursor.execute(query, values)
    conn.commit()

    conn.close()

def order_annuncio_by(annunci, campo, reverse):
    return sorted(annunci, key=lambda x:x[campo], reverse=reverse)