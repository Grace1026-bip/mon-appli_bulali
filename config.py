import os

#Générateur des nouvelles clés secrètes
#>>> import random, string
#>>> "".join([random.choice(string.printable)]) for _in range(24)])
Secret_key ="#d#Jesus_Amours_x...\nilK\\7m\x0bp#\tg#Y"
BULALI_ID = 281129082610170312090405

#pour la connexion avec ma bd
basedir = os.path.abspath(os.path.dirname(__file__))
sqlalchemy_connexion = 'mysql:///' + os.path.join(basedir, 'bulali.db')



























# import mysql.connector
# def infos_etudiants():
#    connexion = mysql.connector(
#          host ="localhost",
#          user ="root",
#          password ="gra10ce26"
#          ma_base ="data_etudiants")
#    curseur = connexion.cursor()
#    curseur.execute("SELECT photos FROM data_etudiants")
#    for (photos,) in curseur:
# 	   print("etudiant:", photos)
# #print(ma_base)