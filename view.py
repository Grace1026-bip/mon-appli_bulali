from flask import Flask, render_template, request, redirect, url_for, flash, session 
from recon_faciale import db_connexion, encodage, detection_visage, compare_visage
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os

bulali= Flask(__name__)

bulali.config['DEBUG'] = True
bulali.secret_key= "123frdestj0"
bulali.config['UPLOAD_FOLDER'] = "images_etudiants"
allowed_extentions = {'jpg', 'jpeg'}

#vérifie si une extension est valide
def verificateur_fichier_valide(nom_file):
	return '.' in nom_file and nom_file.rsplit('.', 1)[1].lower() in allowed_extentions

#Page d'accueil 
@bulali.route("/")
def index():
	return render_template("index.html")

#page à propos
@bulali.route("/Apropos")
def apropos():
	return render_template("apropos_bulali.html")

#pour la reconnaissance + le résultat
@bulali.route("/reconnaissance")
def reconnaissance():
	visage_capture = detection_visage()
	resultat = compare_visage(visage_capture)
	return render_template("resultat.html", message=resultat)

#Enregistrement de l'administrateur
@bulali.route("/enregistrement admin", methods=['GET', 'POST'])
def enregistrement_admin():
	if request.method == "POST":
		nom = request.form["Nom"]
		postnom= request.form["Postnom"]
		prenom = request.form["Prenom"]
		email = request.form["email"]
		password = request.form["password"]
		if not (nom and postnom and prenom and email and password):
			flash("Tous les champs sont obligatoires.")
			return render_template("login.html")
		
		password_hash = generate_password_hash(password)
		mybd = db_connexion()
		cursor = mybd.cursor(dictionary=True)
		try:
			cursor.execute(
			"INSERT INTO admini (adm_nom, adm_postnom, adm_prenom, adm_email, adm_password) VALUES (%s, %s, %s, %s, %s)", 
			(nom, postnom, prenom, email, password_hash))
			mybd.commit()
			print("L'enregistrement a été un ssuccès!")
		except Exception as e:
			print("Echec de l'enregistrement!")
			flash("Erreur! lors de l'enregistrement.")
		finally:
			cursor.close()
			mybd.close()
	return render_template("enregistrement_admin.html")

#la connexion de l'administrateur
@bulali.route("/login", methods = ['GET', 'POST'])
def login_admin():
	if request.method == "POST":
		nom = request.form["Nom"]
		postnom= request.form["Postnom"]
		prenom = request.form["Prenom"]
		email = request.form["email"]
		password_saisi = request.form["password"]

		print(request.form['Nom'])

		conn = db_connexion()
		cursor = conn.cursor(dictionary=True)

		cursor.execute(
			"SELECT * FROM admini WHERE adm_nom =%s AND adm_postnom=%s AND adm_prenom=%s AND adm_email=%s ", 
			(nom, postnom, prenom, email))

		admini = cursor.fetchone() #ramène la table en dictionnaire
		cursor.close()
		conn.close()

		if admini and check_password_hash(admini["adm_password"], password_saisi):
			session["admin_connecte"] = True
			return redirect(url_for("ajout_etudiant"))
		else:
			flash("Informations incorrectes. Veuillez bien vérifier tous les champs", "erreur!")
	return render_template("login.html")

#formulaire d'ajout d'un nouvel étudiant
@bulali.route("/ajout", methods=["GET", "POST"])
def ajout_etudiant():
	if not session.get("admin_connecte"):
		return redirect(url_for("login_admin"))
	
	if request.method == "POST":
		nom = request.form["Nom"]
		postnom = request.form["Postnom"]
		prenom = request.form["Prenom"]
		matricule = request.form["Matricule"]
		fichier = request.files["Photo"]

		if fichier and verificateur_fichier_valide(fichier.filename):
			nom_file = secure_filename(matricule + ".jpg") #on nomme l'image avec le matricule
			chemin = os.path.join(bulali.config['UPLOAD_FOLDER'], nom_file)
			fichier.save(chemin)

			conn= db_connexion()
			cursor= conn.cursor()
			cursor.execute("INSERT INTO etudiants (nom, postnom, prenom, matricule, photos) VALUES (%s, %s, %s, %s,%s)", (nom, postnom, prenom, matricule, chemin))
			conn.commit()
			cursor.close()
			conn.close()

			flash("Etudiant ajouté avec succès.")
			return redirect(url_for("form_ajout"))
		else:
			flash("Fichier invalide. Choisissez une image .jpg")
	return render_template("form_ajout.html")

if __name__ == '__main__':
	bulali.run(debug=True)


