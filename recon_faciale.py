import cv2 as cv
import face_recognition
import os
import pickle
import mysql.connector

#pour la connexion à ma base
def db_connexion():
	return mysql.connector.connect(
		host= "localhost",
		user= "root",
		password= "Gra26ce10",
		database= "data_etudiants"
	)
#l'encodage des visages depuis les images et mise à jour dans ma bd et mise à jour de la bd
def encodage():
	try:
		mybd = db_connexion()
		cursor = mybd.cursor()

		cursor.execute("SELECT id, paths_visages FROM etudiants")
		etudiants = cursor.fetchall()

		for etu in etudiants:
			id_etu = etu[0] 
			path_etu = etu[1]
			chemin_complet = os.path.join("app_bulali", path_etu)

			print(f"Traitement de l'étudiant ID{id_etu}...")

			if not os.path.isfile(chemin_complet):
				print(f"Image introuvable pour {id_etu} : {chemin_complet}")
				continue
			try:
				image = face_recognition.load_image_file(chemin_complet)
				visage= face_recognition.face_locations(image)
			
				if not visage:
					print(f"Aucun visage détecté pour l'étudiant ID{id_etu}")
					continue

				encs = face_recognition.face_encodings(image)
				if not encs:
					print(f"L'encodage pour l'étudiant ID{id_etu} a échoué")
					continue
				enc_premier= encs[0]
				enc_pickel = pickle.dumps(enc_premier)

				cursor.execute("UPDATE etudiants SET encodages = %s WHERE id = %s", (enc_pickel, id_etu))
				mybd.commit()
				print(f"Encodage enregistré pour ID {id_etu}")
			except Exception as err:
				print(f"Erreur avec l'étudiant{id_etu} :", err)
	except Exception as e:
			print("Erreurde connexion à la base")
	finally:
		cursor.close()
		mybd.close()

#récuperer les encodages enregistrés depuis la base
def recuperer_encodages():
	mybd = db_connexion()
	cursor = mybd.cursor()
	cursor.execute("SELECT id, encodages FROM etudiants")
	resultats = cursor.fetchall()

	cursor.close()
	mybd.close()

	Encodages =[]
	for etu_id, encs_bin in resultats:
		if encs_bin:
			try:
				encodage_reel = pickle.loads(encs_bin)
				Encodages.append((etu_id,encodage_reel))
				print("Ouiii, la récupération a marché!")
			except Exception as e:
				print(f"Erreur de décodage pour l'ID {etu_id}:{e}") 
	return Encodages
		
#capture d'un visage en temps réel depuis la caméra
def detection_visage():
	visage = cv.VideoCapture(0)
	encode_etudiant = None
	encode =[]

	while visage.isOpened():
		ret, frame = visage.read()
		if not ret :
			break
		rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
		faces = face_recognition.face_locations(rgb_frame)

		#Vérification si le visage est bien détecté
		for top, right, bottom, left in faces:
			cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
			
		cv.putText(rgb_frame, "Appuyer sur g pour capturer", (10,30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 250), 2)
		cv.imshow("Capture", rgb_frame)

		encode = face_recognition.face_encodings(faces[0])

		if cv.waitKey(1) & 0xFF == ord('g'):
			if encode:
				encode_etudiant = encode[0]#prend le premier visage détecté
				break
	visage.release()
	cv.destroyAllWindows()#pour detruire toute les fenêtres
	return encode_etudiant
			
#comparaison du visage capturé avec les visages encodés en base
def compare_visage(encode_capturer):
	if encode_capturer is None:
		return "❌Aucun visage capturé"
	encodages_enregistres = recuperer_encodages()
	for etu_id, enc_reel in encodages_enregistres:
		resultat = face_recognition.compare_faces([enc_reel], encode_capturer)
		if resultat[0]:
			return f"✅ Etudiant solvable(ID:{etu_id})"
		return "❌Etudiant insolvable"
	
detection_visage()

