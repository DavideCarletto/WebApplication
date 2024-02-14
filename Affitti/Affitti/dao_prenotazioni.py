import sqlite3

column_prenotazioni_names= ["UserID", "Data", "OraInizio", "OraFine", "Tipo", "Stato", "MotivoRifiuto", "AnnuncioID", "prenotazioneID"]
def get_prenotazioni_accettate_from_data(id, data):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Prenotazione WHERE Data = ? AND Stato = 'ACCETTATA' AND AnnuncioID = ?"

    prenotazioni = [dict(zip(column_prenotazioni_names, prenotazione)) for prenotazione in cursor.execute(sql, (data, id)).fetchall()]

    cursor.close()
    conn.close()

    return prenotazioni


def insert_prenotazione(user_id, data, orainizio, orafine, tipo, stato, motivorifiuto, idannuncio):

    success = False
    conn= None

    try:
        conn = sqlite3.connect("db/Affitti.db")
        cursor = conn.cursor()

        sql = "INSERT INTO Prenotazione (UserID, Data, OraInizio, OraFine, Tipo, Stato, MotivoRifiuto, AnnuncioID) VALUES (?,?,?,?,?,?,?,?)"

        cursor.execute(sql, (user_id, data, orainizio, orafine, tipo, stato, motivorifiuto, idannuncio))

        conn.commit()

        cursor.close()
        conn.close()

        success=True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Errore durante l'inserimento della prenotazione: {e}")
        success = False

    finally:
        if conn:
            conn.close()

    return success


def get_richieste_non_rifiutate_annuncio_from_utente(id_annuncio, id_utente):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Prenotazione WHERE UserID = ? and AnnuncioID = ? and Stato <> 'RIFIUTATA'"

    prenotazioni = cursor.execute(sql, (id_utente, id_annuncio)).fetchall()
    prenotazioni = [dict(zip(column_prenotazioni_names, prenotazione))for prenotazione in prenotazioni]

    cursor.close()
    conn.close()
    print(prenotazioni)
    return prenotazioni

def get_prenotazioni_from_utente(id_utente):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Prenotazione WHERE UserID = ?"

    prenotazioni = cursor.execute(sql, (id_utente,)).fetchall()
    prenotazioni = [dict(zip(column_prenotazioni_names , prenotazione)) for prenotazione in prenotazioni]

    cursor.close()
    conn.close()

    return prenotazioni
def get_richieste_prenotazione_from_annuncio(id_annuncio):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()

    sql = "SELECT * FROM Prenotazione WHERE AnnuncioID = ?"

    prenotazioni = cursor.execute(sql, (id_annuncio,)).fetchall()
    prenotazioni = [dict(zip(column_prenotazioni_names, prenotazione)) for prenotazione in prenotazioni]

    cursor.close()
    conn.close()

    return prenotazioni

def change_status_prenotazione(id_preotazione, stato, motivo = None):

    conn = sqlite3.connect("db/Affitti.db")
    cursor = conn.cursor()
    sql = ""

    if stato == "ACCETTATA":
        sql = "UPDATE Prenotazione SET Stato='ACCETTATA' WHERE PrenotazioneID = ?"
        cursor.execute(sql, (id_preotazione, ))
    else:
        sql = "UPDATE Prenotazione SET Stato = 'RIFIUTATA', MotivoRifiuto = ? WHERE PrenotazioneID = ?"
        cursor.execute(sql, (motivo, id_preotazione))

    conn.commit()

    cursor.close()
    conn.close()

    return
