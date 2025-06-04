from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

bulali = Flask(__name__)

@bulali.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	bulali.run(debug=True)

