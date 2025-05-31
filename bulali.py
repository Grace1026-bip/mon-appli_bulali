from flask import Flask, render_template, request

bulali = Flask(__name__)

@bulali.route("/")
def accueil():
	return render_template("templates/index.htmll")

if __name__ == "__main__":
	bulali.run(debug=True)

@bulali.route("/admin")
def page_admin(nom, motdepasse):
	return render_template("templates/connexion_admin.html")

@bulali.route("/form")
def page_form():
	return render_template("templates/form_ajout.html")
