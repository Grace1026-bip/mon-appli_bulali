import cv2 as cv
import face_recognition
import mysql.connector
from datetime import datetime
import os
import numpy
import pickle


#pour charger le classificateur Haar 
def db_connexion():
	return mysql.connector.connect(
		host="localhost",
		user="root",
		password="Gra26ce10",
		database="data_etudiants"
	)

def connexion_table():
	table = db_connexion()
	cursor = table.cursor()
	result_pv = cursor.execute("SELECT id, paths_visages FROM etudiants")
	return result_pv

def encodage():
	connus = db_connexion()
	cursor = connexion_table()
	for etu_id, path in cursor:
		if not os.path.isfile(path):
			continue
		image = face_recognition.load_image_file(path)
		caractere = face_recognition.face_landmarks(image)
		encs = face_recognition.face_encodings(caractere)
		if not encs:
			continue
		encs_binaire = pickle.dumps(encs[0])
		cursor.execute("UPDATE etudiants SET encodages = %s WHERE id = %s", (encs_binaire, etu_id))
	connus.commit()
	cursor.close()
	connus.close()

def colonne_encodage():
	conn = db_connexion()
	cursor = conn.cursor()
	result = cursor.execute("SELECT encodages FROM etudiants")
	return result

def detection_visage():
	visage = cv.VideoCapture (0)#pour ouvrir la caméra initial
	while(visage.isOpened()):
		ret, frame = visage.read()
		rgb_visage = frame[:, :, ::-1]
		caractere = face_recognition.face_landmarks(rgb_visage)
		encode = face_recognition.face_encodings(caractere)
		if not ret:
			break
		faces = face_recognition.face_locations(rgb_visage)
		for top, right, bottom, left in faces:
			cv.rectangle(frame, (left, top), (right, bottom), (255, 0 , 0), 2)
		cv.imshow("capture", frame)
		if cv.waitKey(1) & 0xFF == ord('g') :#permet de désactiver la caméra si l'on clique sur la lettre entrée en paraméttre
			break
	visage.release() #pour
	cv.destroyAllWindows() #pour detruire toute les fenêtres
def compare_visages(): #comparaison ses visages
	visages_encodes = colonne_encodage()
	for (v, ) in visages_encodes:
		if 
