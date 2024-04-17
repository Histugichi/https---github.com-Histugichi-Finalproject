from flask import Flask, render_template, request, session, url_for, redirect

import bcrypt

from users.user_dao import UserDao
from users.user import User
from evenements.evenement import Evenement
from evenements.evenement_dao import EvenementDao
from paiements.paiement import Paiement
from paiements.paiement_dao import PaiementDao
from reservations.reservation_dao import ReservationDao
from reservations.reservation import Reservation
from reservations.statut import ReservationStatut


app = Flask(__name__,)
app.secret_key = 'secretkey'
salt = bcrypt.gensalt(rounds=12)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/accueil')
def accueil():
    return render_template('accueil.html')


@app.route('/login',methods= ['POST', 'GET'])
def login():
    req = request.form
    message =None
    user = None

    if request.method == "POST":
        username = req ['username']
        password = req ['password']     
        password = password.encode()
        if username=="" or password=="":
            message="error"
        else:
            # Chercher hashed password de la base de donnée base sur username
            message, user = UserDao.get_one(username)
            hashed_password_bd = user[2]
         
            if hashed_password_bd:
                hashed_password_bd = hashed_password_bd.encode()
                # Verifier si le mot de passe est correct
            if bcrypt.checkpw(password, hashed_password_bd):
                    message = 'success'
                   
                    if user:
                        session['nom_complet']=user[0] #On met le nom complet dans notre variable de session
                        session['username']=user[1] # On met le username dans notre variable de session
                         
                        if user[3] ==1: #verifier si c'est un admin, sinon rediriger vers la page de reservation
                            return redirect(url_for('admin'))
                        else:
                            return redirect(url_for("accueil"))  
        message= 'Username et password invalide'
    return render_template('login.html', message=message, user=None)

@app.route('/registrer',methods= ['POST', 'GET'])
def registrer():
    req = request.form
    message =None
    user= None

    if request.method == "POST":
        nom_complet = req ['nom_complet']
        username = req ['username']
        password = req ['password']
        #Hash password
        is_admin= 0
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        
        if nom_complet=="" or username=="" or password=="" :
            message="error"
        else:
            user = User(nom_complet, username, hashed_password, is_admin)
            message = UserDao.create(user)
        print(message)
    return render_template('registrer.html', message=message, user=user)

@app.route('/evenement')
def evenement():
    message, evenements=EvenementDao.get_all()
    return render_template('evenement.html', message=message, evenements=evenements)

@app.route('/add_event', methods= ['POST', 'GET'])
def add_event():
    req = request.form
    message=None
    evenement=None

    if request.method == "POST":
        nom = req ['nom']
        date = req ['date']
        emplacement = req ['emplacement']
        prix = req ['prix']
        
        if nom=="" or date=="" or emplacement=="" or prix=="":
            message="error"
        else:
            evenement = Evenement(nom,date,emplacement,prix)
            message = EvenementDao.create_evenement(evenement)
            print(message)
    return render_template('add_event.html', message=message, evenement=evenement)

@app.route('/modify_event')
def modify_event():
    message, evenements=EvenementDao.modifier_evenement()
    return render_template('modify_event.html', message=message, evenements=evenements)

@app.route('/delete_event')
def delete_event():
    message, evenements=EvenementDao.supprimer_evenement()
    return render_template('delete_event.html', message=message, evenements=evenements)

@app.route('/statut')
def statut():
    message, reservation = ReservationStatut()
    return render_template('statut.html', message=message, reservation=reservation)


@app.route('/historique')
def historique():
    return render_template('historique.html')

@app.route("/logout")
def logout():
    session.clear() # On vide la session
    return redirect(url_for('login'))

@app.route('/reservations', methods=['POST', 'GET'])
def reservations():
    nom=None
    date=None
    statut=None
    if request.method == 'POST':
        nom = request.form['nom']
        date = request.form['date']
        statut = request.form['statut']
        if nom=="" or date=="" or statut=="" :
            message="error"
        else:
            reservation = Reservation(nom, date, statut)
            message = ReservationDao.reserver_place(reservation)
            print(message)
        return redirect(url_for('paiement'))
    return render_template('reservations.html', nom=nom, date=date, statut=statut)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    message, users = UserDao.list_all()
    return render_template('liste_users.html', message= message, users= users)

@app.route('/add-users', methods= ['POST', 'GET'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    req = request.form
    message =None
    user= None

    if request.method == "POST":
        nom_complet = req ['nom_complet']
        username = req ['username']
        password = req ['password']
        type = req ['type']

        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        
        if nom_complet=="" or username=="" or password=="" or type=="":
            message="error"
        else:
            user = User(nom_complet,username,hashed_password, type)
            message = UserDao.create(user)
        print(message)
    return render_template('add_users.html', message= message, user=user)



@app.route('/paiement', methods=['POST','GET'])
def paiement():
    montant=None
    mode_paiement=None
    id_paiement=None
    date=None
    cvv=None
    
    if request.method == 'POST':
        montant = request.form['card_number']
        mode_paiement= request.form['mode_paiement']
        id_paiement=request.form['id_paiement']
        date=request.form['date']
        cvv = request.form['cvv']

        if montant=="" or mode_paiement=="" or id_paiement=="" or date=="" or cvv=="":
            message="error"
        else:
            paiement= Paiement(montant,mode_paiement,id_paiement,date,cvv)
            message = PaiementDao.ajouter_paiement(paiement)
        return redirect(url_for('confirmation'))
    return render_template('paiement', message=message, paiement=paiement)


if __name__ == "__main__":
    app.run(debug=True)
