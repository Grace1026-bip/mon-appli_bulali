from flask_sqlalchemy import SQLAlchemy

from .view import bulali

data_etudiants = SQLAlchemy(bulali)
class etudiants(data_etudiants.Model):
	id= data_etudiants.Column(data_etudiants.Integer, primary_key=True)
	nom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	postnom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	prenom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	photos = data_etudiants.Colum(data_etudiants.String(200), nullable=False)
	encodage= data_etudiants.Colum(data_etudiants.String(300), nullable=False)