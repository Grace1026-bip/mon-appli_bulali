from flask_sqlalchemy import SQLAlchemy
import logging as lg
from .view import bulali
import os


bulali.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:Gra26ce10@localhost/data_etudiants'
bulali.config['SQLAlCHEMY_TRACK_MODIFICATIONS']= False

data_etudiants = SQLAlchemy(bulali)
 
dossier_visages= "static/images_bulali"
os.makedirs(dossier_visages, exist_ok=True)

class Etudiants(data_etudiants.Model):
	__tablename__='etudiants'

	id= data_etudiants.Column(data_etudiants.Integer, primary_key=True)
	nom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	postnom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	prenom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	matricule = data_etudiants.Column(data_etudiants.String(50), unique= True, nullable=False)
	photos = data_etudiants.Colum(data_etudiants.String(200), unique=True, nullable=False)
	encodages= data_etudiants.Colum(data_etudiants.String(300), unique=True, nullable=False)

		




