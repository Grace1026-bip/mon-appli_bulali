from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from recon_faciale import db_connexion, recuperer_encodages, encodage, detection_visage, compare_visages
from werkzeug.utils import secure_filename
import os


bulali = Flask(__name__)

bulali.secret_key= "123frdestj0"
bulali.config.from_object('config')
allowed_extentions = {'jpg', 'jpeg'}

@bulali.route("/Apropos")
def apropos():
	return render_template("apropos_bulali.html")

@bulali.route("/Reconnaissance")
def reconnaissance():
	encodage()
	visage_capture = detection_visage()
	resultat = compare_visages(visage_capture)
	return render_template("/")

@bulali.route("/connexion_admin")
def conn_admin():
	nom = request.form["Nom"]
	postnom = request.form["Postnom"]
	prenom = request.form["Prenom"]
	email = request.form["email"]
	
	return render_template("connexion_admin.html")

@bulali.route("/ajout",  methods=["POST"])
def new_etudiant ():
	nom = request.form["Nom"]
	postnom = request.form["Postnom"]
	prenom = request.form["Prenom"]
	matricule = request.form["Matricule"]
	photos = request.form["Photo"]

	conn= db_connexion()
	cursor= conn.cursor()
	cursor.execute("INSERT INTO etudiants (nom, postnom, prenom, matricule, photos) , (%s, %s, %s, %s,%s)")
	
	return render_template("form_ajout.html")
	


@bulali.route("/")
def index():
	return render_template("index.html")


	