import cv2 as cv
import face_recognition
import mysql.connector
from datetime import datetime
import os
import numpy
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
	cursor.execute("SELECT * FROM etudiants")


def detection_visage():
	visage = cv.VideoCapture (0)#pour ouvrir la caméra initial
	while(visage.isOpened()):
		ret, frame = visage.read()
		rgb_visage = frame[:, :, ::-1]
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