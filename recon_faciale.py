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
#l'encodage des visages depuis les images et mise à jour dans ma bd
def encodage():
	mybd = db_connexion()
	cursor = mybd.cursor()

	cursor.execute("SELECT id, paths_visages FROM etudiants")
	for etu_id, path in cursor :
		if not os.path.isfile(path):
			print(f"⚠ Image non trouvéé pour ID{etu_id}:{path}")
			continue
		image = face_recognition.load_image_file(path)
		encs = face_recognition.face_encodings(image)
		if not encs :
			continue
		encs_bin = pickle.dumps(encs[0])
		cursor.execute("UPDATE etudiants SET encodages = %s WHERE id= %s", (encs_bin, etu_id))
	mybd.commit()
	cursor.close()
	mybd.close()
	print("✅ Encodage des visages terminés")

#récuperer les encodages depuis la base
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
			except Exception as e:
				print(f"Erreur de décodage pour l'ID {etu_id}:{e}") 
				return Encodages
#capture d'un visage en temps réel depuis la caméra
def detection_visage():
	print("📸 Appuyer sur 'g' pour capturer un visage")
	visage = cv.VideoCapture(0)
	encode_etudiant = None

	while visage.isOpened():
		ret, frame = visage.read()
		if not ret :
			break
		rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
		faces = face_recognition.face_locations(rgb_frame)
		encode = face_recognition.face_encodings(rgb_frame, faces)
		#Vérification si le visage est bien détecté
		for top, right, bottom, left in faces:
			cv.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
		cv.putText(frame, "Appuyer sur g pour capturer", (10,30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
		cv.imshow("Capture", frame)
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
	if __name__=="main":
		print("Lancement du processus de reconnaissance faciale")
		visage_capture = detection_visage()
		resultat = compare_visage(visage_capture)
		print(resultat)

