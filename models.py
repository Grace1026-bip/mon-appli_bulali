from flask_sqlalchemy import SQLAlchemy

from .route import bulali

data_etudiants = SQLAlchemy(bulali)
class etudiants(data_etudiants.Model):
	id= data_etudiants.Column(data_etudiants.Integer, primary_key=True)
	description = data_etudiants.Colum(data_etudiants.String(200), nullable=False)
	
