import sys, os

from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

sys.path.append("..")
from steg import encrypt, decrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'evillaugh'
app.config['ENCRYPT_UPLOAD_FOLDER'] = 'uploads/encrypt/'
app.config['DECRYPT_UPLOAD_FOLDER'] = 'uploads/decrypt/'

@app.route("/", methods=["GET", "POST"])
def base():
	return render_template("index.html")


@app.route("/encrypt", methods=["GET", "POST"])
def encrypter():
	if request.method =="POST":
		secret_type = request.form["type"]
		f = request.files['cover']
		filename = secure_filename(f.filename)
		f.save(app.config['ENCRYPT_UPLOAD_FOLDER'] + filename)
		path1 = os.path.abspath(app.config['ENCRYPT_UPLOAD_FOLDER'] + filename)
		f = request.files['steg']
		filename = secure_filename(f.filename)
		f.save(app.config['ENCRYPT_UPLOAD_FOLDER'] + filename)
		path2 = os.path.abspath(app.config['ENCRYPT_UPLOAD_FOLDER'] + filename)
		if secret_type == "photo":
			path = encrypt.steg_photo(path1, path2)
		else:
			path = encrypt.steg_video(path1, path2)
		return send_file(path, as_attachment=True)
		
	return render_template("encrypt.html")

@app.route("/decrypt", methods=["GET", "POST"])
def decrypter():
	if request.method =="POST":
		secret_type = request.form["type"]
		f = request.files['data']
		filename = secure_filename(f.filename)
		f.save(app.config['DECRYPT_UPLOAD_FOLDER'] + filename)
		path = os.path.abspath(app.config['DECRYPT_UPLOAD_FOLDER'] + filename)
		if secret_type == "photo":
			path = decrypt.steg_photo(path)
		else:
			path = decrypt.steg_video(path)
		return send_file(path, as_attachment=True)
	return render_template("decrypt.html")
	

