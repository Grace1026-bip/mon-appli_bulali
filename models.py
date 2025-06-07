from flask_sqlalchemy import SQLAlchemy
import logging as lg
from .view import bulali

data_etudiants = SQLAlchemy(bulali)

class etudiants(data_etudiants.Model):
	id= data_etudiants.Column(data_etudiants.Integer, primary_key=True)
	nom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	postnom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	prenom = data_etudiants.Colum(data_etudiants.String(100), nullable=False)
	photos = data_etudiants.Colum(data_etudiants.String(200), unique=True, nullable=False)
	encodages= data_etudiants.Colum(data_etudiants.String(300), unique=True, nullable=False)

	def _init_(self, nom, postnom, prenom, photos, encodages):
		self.nom = nom
		self.postnom = postnom
		self.prenom = prenom
		self.photos = photos
		self.encodages = encodages
		
data_etudiants.create_all()

def init_db():
	data_etudiants.drop_all()
	data_etudiants.create_all()
	data_etudiants.session.add(etudiants("c'est partaa", 1))
	data_etudiants.session.add(etudiants("moi toi toi moi", 0))
	data_etudiants.session.commit()
	lg.warning('Database initialisé')