import cv2 as cv
import face_recognition
import mysql.connector
from datetime import datetime
import os
import numpy
import pickle

#pour me conecter à ma base
def db_connexion():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="Gra26ce10",
		database="data_etudiants"
	)
#encodage des visages depuis les images et mise à jour dans la base de données
def encodage():
	conn = db_connexion()
	cursor = conn.cursor()

	cursor.execute("SELECT id, paths_visages FROM etudiants")
	for etu_id, path in cursor:
		if not os.path.isfile(path):
			continue
		image = face_recognition.load_image_file(path)
		encs = face_recognition.face_encodings(image)
		if not encs:
			continue
		encs_binaire = pickle.dumps(encs[0])
		cursor.execute("UPDATE etudiants SET encodages = %s WHERE id = %s", (encs_binaire, etu_id))
	conn.commit()
	cursor.close()
	conn.close()

#recupère  tous les encodages enregistrés depuis la base de données
def recuperer_encodages():
	conn = db_connexion()
	cursor = conn.cursor()
	cursor.execute("SELECT id, encodages FROM etudiants")
	resultats = cursor.fetchall()
	Encodages = []
	for etu_id, enc_bin in resultats:
		if enc_bin is not None:
			encodage_reel = pickle.loads(enc_bin)
			Encodages.append((etu_id, encodage_reel))
	cursor.close()
	conn.close()
	return Encodages

#capture d'un visage en temps réel dépuis la caméra
def detection_visage():
	global encode_etudiant
	encode_etudiant = None

	visage = cv.VideoCapture (0)
	while visage.isOpened():
		ret, frame = visage.read()
		if not ret :
			break
		rgb_frame = frame[:, :, ::-1]
		faces = face_recognition.face_locations(rgb_frame)
		encode = face_recognition.face_encodings(rgb_frame, faces)

		for top, right, bottom, left in faces:
			cv.rectangle(frame, (left, top), (right, bottom), (255, 0 , 0), 2)

		cv.imshow("Capture", frame)

		if cv.waitKey(1) & 0xFF == ord('g') :#permet de désactiver la caméra si l'on clique sur la lettre entrée en paraméttre
			if encode :
				encode_etudiant = encode[0] #prend lepremier visage détecté
			break
	visage.release() #pour
	cv.destroyAllWindows() #pour detruire toute les fenêtres

#Comparaison du visage capturé avec les visages encodés en base
def compare_visages(): #comparaison ses visages
	if encode_etudiant is None:
		return "Aucun visage capturé"
	encodages_enregistres = recuperer_encodages()
	for etu_id, enc_reel in encodages_enregistres:
		resultat = face_recognition.compare_faces([enc_reel], encode_etudiant)
		if resultat[0]:
			return f"Etudiant solvable (ID: {etu_id})"
	return "Etudiant insolvable"
		
encodage()
