from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from recon_faciale import db_connexion
from models import Etudiants

bulali = Flask(__name__)

bulali.config.from_object('config')

@bulali.route("/")
def index():
	etudiants = Etudiants.query.all()
	return '<br>'.join([e.nom for e in etudiants])
@bulali.route("/enregistrement")
def enregistrement_form():
	return render_template("connexion_admin.html")

@bulali.route("/ajouter" , mathods=["POST"])
def new_etudiant():
	nom = request.form["Nom"]
	postnom = request.form["Postnom"]
	prenom = request.form["Prénom"]
	matricule = request.form["Matricule"]
	photos = request.form["Photo"]

	conn= db_connexion()
	cursor= conn.cursor()
	cursor.execute("INSERT INTO etudiants (nom, postnom, prenom, matricule, photos) , ")
	return
