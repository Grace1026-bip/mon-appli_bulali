import cv2 as cv
import face_recognition
import os
import numpy
import json 

#pour charger le classificateur Haar 
def reconnaissance_facials():
	face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
	visage = cv.VideoCapture (0)#pour ouvrir la caméra initial
	visage.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
	#la boucle permet de lire chaque trame de la vidéo et lire directement la vidéo si la caméra est ouverte
	while (visage.isOpened()):
		ret, frame = visage.read()
		if not ret :
			break
		faces = face_cascade.detectMultiScale(frame, 1.1, 5)
		for(x, y, w, h) in faces :
			centre_x, centre_y = x + w //2, y + h // 2 #le centre du visage
			rect_w, rect_h = w, h  #ajuste la taille du rectangle
			#calcule les coins du rectangle
			x1 = centre_x - rect_w // 2
			y1 = centre_y - rect_h // 2
			x2 = centre_x + rect_w//2
			y2 = centre_y + rect_h//2
			#dessin du rectangle vert
			cv.rectangle(frame, (x1, y1), (x2, y2), (112, 0, 0), 3)
		#frame = cv.cvtColor( frame, cv.COLOR_BGR2RGB)
	cv.imshow("capture", frame) #pour ouvrir une fenê tre où apparait la camérra
	if cv.waitKey(1) & 0xFF == ord('g') : #permet de désactiver la caméra si l'on clique sur la lettre entrée en paraméttre
		visage.release() #pour
		cv.destroyAllWindows() #pour detruire toute les fenêtres

#def ouvre_dossier(dossier_ouverture):
	#dossier_ouverture 
reconnaissance_facials()

	
