from flask import Flask as flask, render_template, request, redirect, session
from cryptography.fernet import Fernet as fernet
import json
import os
import datetime

app = flask(__name__)
status = None
app.secret_key = "rahasia_banget"
keyuser = fernet(b"_JGnUepJSDVSYLdxdc4yohL306GT57y84Qwfig0ahmc=")  # ni cuma ngasal biar function dekrip sama enkrip g error

def enkrip(text):
    return keyuser.encrypt(text.encode()).decode()

def dekrip(text):
    return keyuser.decrypt(text.encode()).decode()

if os.path.exists("data.json"):
	with open("data.json", "r") as read:
		data = json.load(read)
		key = None
else:
	data = {"tesvalid": "", "teks": []}
	key = fernet.generate_key()
	f = fernet(key)
	enkrip_awal = f.encrypt(b"ini valid")
	utf_nkrip_awal = enkrip_awal.decode('utf-8')
	data["tesvalid"] = utf_nkrip_awal


@app.route("/", methods=["GET", "POST"])
def index():
	status = None
	if request.method == "POST":
		try:
			user = request.form["nama"]
			keyuser = fernet(bytes(user, "utf-8"))
			if keyuser.decrypt(data["tesvalid"].encode()).decode() == "ini valid":
				status = "login berhasil"
				print("login berhasil")
				print(data)
				session["login"] = True

				return redirect("/home/")

		except Exception:
			status = "password salah"
			print("password salah")
	if key:
		return render_template("index.html", password=key.decode(), status=status)
	else:
		return render_template("index.html", status=status)


@app.route("/home/", methods=["GET", "POST"])
def home():
	if not session.get("login"):
		return redirect("/")

	data_dekrip = {"teks":[]}
	if data["teks"]:
		for i in range(0, len(data["teks"])):
			data_dekrip["teks"].append({
				"username" : data["teks"][i]['username'], 
				"label"    : data["teks"][i]['label'], 
				"password" : dekrip(data["teks"][i]['password']),
				"created"  : data["teks"][i]['created'],
			})

	if request.method == "POST":
		label = request.form["label"]
		username = request.form["username"]
		password = request.form["password"]

		tanggal = datetime.datetime.now()
		format_tanggal = f"{tanggal.strftime('%d')} {tanggal.strftime('%B')} {tanggal.strftime('%Y')}"

		data["teks"].append({
			"username" : username.upper(),
			"label"    : label,
			"password" : enkrip(password),
			"created"  : format_tanggal
		})
		return redirect("/home/")

	return render_template("home.html", data=data_dekrip)

@app.route("/logout")
def logout():
	if not session.get("login"):
		return redirect("/")
	session.clear()
	with open("data.json", "w") as f:
		f.write(json.dumps(data))
		return redirect("/")

@app.route("/delete/<int:index>")
def hapus(index):
	if not session.get("login"):
		return redirect("/")

	data["teks"].pop(index)
	print(data)

	return redirect("/home")

@app.route("/edit", methods=["POST"])
def edit_data():
    if not session.get("login"):
        return redirect("/")
        
    idx = int(request.form["index"])
    
    # Update data berdasarkan lookup dictionary mirip CLI kamu dulu
    data["teks"][idx]["label"] = request.form["label"].upper()
    data["teks"][idx]["username"] = request.form["username"]
    data["teks"][idx]["password"] = enkrip(request.form["password"])
    # Tanggal dibuat tidak perlu diubah agar tetap melacak waktu asli pembuatan

    return redirect("/home/")
app.run(debug=True)