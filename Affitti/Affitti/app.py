from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime, timedelta
from flask_login import LoginManager, login_required, login_user, current_user
import dao_annunci
import dao_foto
import dao_prenotazioni
import dao_utenti
from werkzeug.security import generate_password_hash, check_password_hash

import os

from Models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

error_msg = ""
sign_error = ""
fasce_orarie = ["9-12", "12-14", "14-17", "17-20"]

# error_msg mi serve per analizzare errori nel login
@app.route('/', methods=['GET', 'POST'])
def index():
    global error_msg
    annunci = dao_annunci.get_annunci_disponibili(short_address=True)
    # print(annunci)
    sort_price = request.form.get("sort")
    print(sort_price)
    if sort_price is not None:
        annunci = dao_annunci.order_annuncio_by(annunci, "locali", False)
    else:
        annunci = dao_annunci.order_annuncio_by(annunci, "prezzo", True)

    if annunci is None:
        annunci = dict()

    show_login = False
    if len(error_msg)>0:
        show_login = True
        flash(error_msg, 'danger')

    return render_template("index.html", message = error_msg, show_login = show_login, annunci = annunci)

@app.route("/register")
def register():
    global error_msg
    error_msg = ""
    return render_template("register.html", error_msg = sign_error)


@app.route("/sign", methods=['POST'])
def sign():
    user = request.form.to_dict()
    error_status = False
    global  sign_error

    if len(user["username"]) == 0:
        sign_error = "Inserisci un nome valido."
        error_status = True
    if len(user["password"]) == 0:
        sign_error = "Password non valida. Riprovare."
        error_status = True
    if user["password"] != user["rptPassword"]:
        sign_error = "Le due password non coincidono. Riprovare,"
        error_status = True

    userfind = dao_utenti.get_user_from_email(user["email"])

    if userfind is not None:
        sign_error = "Email già in uso."
        error_status=True

    if error_status is True:
        return redirect(url_for("register"))

    password_hash = generate_password_hash(user["password"], method='pbkdf2:sha256')

    user["password"] = password_hash

    if "type" in user:
        user["type"] = "LOCATORE"
    else:
        user["type"] = "CLIENTE"

    success = dao_utenti.insert_user(user)

    if success is False:
        sign_error="Errore di connessione al server. Riprovare."
        return redirect(url_for("register"))

    return redirect("/")

@app.route("/login", methods=['POST'])
def login():

    user = request.form.to_dict()
    global error_msg
    match = dao_utenti.get_user_from_email(user["email"])
    error_msg = ""
    if match is None:
        error_msg = "Email non valida. Riprovare."
    else:
        if not check_password_hash(match["Password"], user["password"]):
            error_msg = "Password non valida. Riprovare."

    if len(error_msg) > 0:
        return redirect(url_for("index"))
    new = User(id=match['UserID'], email=match['Email'], psd=match['Password'], username=match['Username'],type=match['Type'])
    login_user(new, True)
    return redirect(url_for("index"))

@app.route("/annuncio/<int:id>", methods=['POST', 'GET'])
def show_annuncio(id):
    images = dao_foto.get_foto_from_annuncio(id)
    annuncio = dao_annunci.get_annuncio_from_id(id)
    prenotabile = dao_annunci.is_prenotabile(id)
    annuncio["images"]=dict()
    image_button_clicked = request.form.get('image_button')
    if image_button_clicked is not None:
        for image in images:
            if image["percorsoFoto"] == image_button_clicked:
                image["main"] = "SI"
            else:
                image["main"] = "NO"

    annuncio["images"] = images
    annuncio["userid"] = dao_utenti.get_email_from_id(annuncio["userid"])
    print(annuncio)
    return render_template("annuncio.html", id= id, annuncio=annuncio, prenotabile = prenotabile)

# status prende il bottone cerca orari per capire se visualizzare gli orari disponibili (possibile solo dopo
# la scelta della data). In caso affermativo si visualizzano gli orari disponibili per quell'annuncio
@app.route("/prenota/<int:id>", methods=['POST'])
@login_required
def prenota(id):
    annuncio = dao_annunci.get_annuncio_from_id(id)
    foto = dao_foto.get_main_foto_from_annuncio(id)
    status = request.form.get("cerca-orari")
    oredisponibili = ""
    data = ""
    tipo = ""
    data_corrente = datetime.now()
    data_massima = data_corrente + timedelta(days=7)

    data_corrente = data_corrente.strftime('%Y-%m-%d')
    data_massima = data_massima.strftime('%Y-%m-%d')
    if status == "cercaorari":
        data = request.form.get("data")
        tipo = request.form.get("tipo")
        oredisponibili = fasce_orarie.copy()
        prenotazioni_accettate = dao_prenotazioni.get_prenotazioni_accettate_from_data(id, data)
        for ora in fasce_orarie:
            for prenotazione in prenotazioni_accettate:
                if prenotazione["OraInizio"] in ora.split("-")[0]:
                    oredisponibili.remove(ora)



    annuncio["percorsoFoto"] = foto
    return render_template("prenotazione.html", id = id, annuncio =annuncio, status= status, oredisponibili=oredisponibili, data=data, tipo = tipo, data_corrente = data_corrente, data_massima = data_massima)


@app.route("/effettua_prenotazione/<int:id_annuncio>/<string:data>/<string:tipo>", methods=['POST'])
@login_required
def effettua_prenotazione(id_annuncio, data, tipo):
    fasciaoraria = request.form.get("orario-submit")
    success = dao_prenotazioni.insert_prenotazione(current_user.id, data, fasciaoraria.split("-")[0], fasciaoraria.split("-")[1], tipo, "RICHIESTA", None, id_annuncio)

    if success is True:
        flash("Prenotazione avvenuta con successo!", "success")
    # annuncio = dao_annunci.get_annuncio_from_id(id_annuncio)
    return redirect(url_for("show_annuncio", id= id_annuncio))


@app.route("/tueprenotazioni")
@login_required
def tueprenotazioni():
    prenotazioni = dao_prenotazioni.get_prenotazioni_from_utente(current_user.id)

    for prenotazione in prenotazioni:
        fotopath = dao_foto.get_main_foto_from_annuncio(prenotazione["AnnuncioID"])

        if fotopath is not None:
            prenotazione["mainfoto"] = fotopath
            prenotazione["Stato"]= prenotazione["Stato"].lower()

    return render_template("tueprenotazioni.html", prenotazioni= prenotazioni)


@app.route("/tuoiannunci")
@login_required
def tuoiannunci():

    annunci = dao_annunci.get_annunci_good_format(dao_annunci.get_annunci_from_userID(current_user.id), short_address=True)
    noreq = True
    for annuncio in annunci:
        annuncio["richieste"] =dao_prenotazioni.get_richieste_prenotazione_from_annuncio(annuncio["id"])
        # print(len(annuncio["richieste"]))
        if len(annuncio["richieste"])>0:
            noreq = False

        for richiesta in annuncio["richieste"]:
            email_utente = dao_utenti.get_email_from_id(richiesta["UserID"])
            richiesta["email"] = email_utente
    # print(annunci)
    return render_template("tuoiannunci.html", annunci= annunci, noreq = noreq)

# controllo se la richiesta mi è arrivata dal bottone di rifiuta o di accetta per capire come comportarmi sulla richiesta
@app.route("/richiesta",  methods=['POST', 'GET'])
@login_required
def azione_richiesta():

    rifiuta = request.form.get("rifiuta-richiesta")
    accetta = request.form.get("accetta-richiesta")

    if rifiuta is not None:
        stato = "RIFIUTATA"
        motivo = request.form.get("motivo-rifiuto")
        print("motivo:" + motivo)
        dao_prenotazioni.change_status_prenotazione(rifiuta, stato, motivo)
    else:
        stato = "ACCETTATA"
        dao_prenotazioni.change_status_prenotazione(accetta, stato)

    return redirect(url_for("tuoiannunci"))

@app.route("/aggiungi", methods = ["POST"])
@login_required
def aggiungi_annuncio():
    annuncio= dict()

    annuncio["titolo"] = request.form.get("titolo")
    annuncio["indirizzo"] = request.form.get("via")+", "+request.form.get("numerocivico")+", "+request.form.get("citta")
    annuncio["tipo"] = request.form.get("tipo")
    annuncio["descrizione"] = request.form.get("descrizioneannuncio")
    annuncio["n_locali"] = request.form.get("numlocali")
    annuncio["arredata"] = "SI" if request.form.get("arredata") is not None else "NO"
    annuncio["disponibile"] = "SI" if request.form.get("disponibile") is not None else "NO"
    annuncio["prezzo"] = request.form.get("prezzo")
    annuncio["images"] = []

    for img in request.files.getlist("images"):
        annuncio["images"].append(img)

    dao_annunci.aggiungi_annuncio(annuncio)

    return redirect(url_for("tuoiannunci"))
@app.route("/elimina_annuncio", methods = ["POST"])
@login_required
def elimina_annuncio():

    annuncio_id = request.form.get("elimina-annuncio-btn")
    dao_annunci.delete_annuncio_from_id(annuncio_id)

    return redirect(url_for("tuoiannunci"))

# prendo ogni campo dell'annuncio e lo mando alla pagina per la modifica
@app.route("/modifica/<int:id>")
@login_required
def modifica_annuncio(id):
    images = dao_foto.get_foto_from_annuncio(id)
    annuncio = dao_annunci.get_annuncio_from_id(id)
    annuncio["via"]= annuncio["indirizzo"].split(",")[0]
    annuncio["n_civico"]= annuncio["indirizzo"].split(",")[1]
    annuncio["citta"]= annuncio["indirizzo"].split(",")[2]
    annuncio["images"] = dict()
    image_button_clicked = request.form.get('image_button')
    if image_button_clicked is not None:
        for image in images:
            if image["percorsoFoto"] == image_button_clicked:
                image["main"] = "SI"
            else:
                image["main"] = "NO"

    annuncio["images"] = images
    print(images)
    annuncio["userid"] = dao_utenti.get_email_from_id(annuncio["userid"])
    # print(annuncio)
    return render_template("modifica_annuncio.html", id=id, annuncio=annuncio)
@app.route("/effettua_modifica/<int:id>", methods = ["POST"])
@login_required
def effettua_modifica(id):
    titolo = request.form.get("titolo")

    tipo = request.form.get("tipo")
    locali = request.form.get("locali")
    prezzo = request.form.get("prezzo")
    arredata = request.form.get("arredata")
    descrizione = request.form.get("description")
    disponibile = request.form.get("disponibile")
    print(titolo, tipo, locali, prezzo, arredata, descrizione)

    if len(tipo)!= 0 or  len(locali)!= 0 or len(prezzo)!=0 or len(arredata)!=0 or len(descrizione)!=0 or len(disponibile)!=0:
        dao_annunci.modifica_annuncio_from_id(id, titolo, tipo, locali, descrizione,prezzo, arredata, disponibile )

    return redirect(url_for('tuoiannunci'))

@app.route("/elimina_foto/<int:id>")
@login_required
def elimina_foto(id):
    id_annuncio = dao_foto.get_id_annuncio_from_foto(id)
    images = dao_foto.get_foto_from_annuncio(id_annuncio)
    if len(images) > 1:
        for image in images:
            if image["main"] == "SI" and image["id"] == id:
                for image_no_main in images:
                    if image_no_main["main"] == "NO":
                        # image_no_main["main"] = "SI"
                        dao_foto.set_main(image_no_main["id"])
                        print("Stato cambiato")
                        break

        dao_foto.delete_foto(id)
    return redirect(url_for("modifica_annuncio", id = id_annuncio))
@app.route("/aggiungi_foto/<int:id_annuncio>", methods = ['POST'])
@login_required
def aggiungi_foto(id_annuncio):
    images = request.files.getlist("images")
    n = len(dao_foto.get_foto_from_annuncio(id_annuncio))
    count= n

    for image in images:
        if count<5:
            dao_foto.insert_photo_in_annuncio(id_annuncio, f"Images/{image.filename}")
            count+=1
        else:
            break

    return redirect(url_for("modifica_annuncio", id = id_annuncio))

@login_manager.user_loader
def load_user(user_id):
    db_user = dao_utenti.get_user_from_id(user_id)
    if db_user is not None:
        user = User(id=db_user['UserID'], email=db_user['Email'],	psd= db_user['Password'], username=db_user['Username'], type = db_user["Type"])
    else:
        user = None

    return user

if __name__ == '__main__':
    app.run()
