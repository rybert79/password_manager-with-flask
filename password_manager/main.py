from flask import Flask as flask, render_template, request, redirect, session
from cryptography.fernet import Fernet as fernet
import json
import os
import datetime
import threading  

app = flask(__name__)
app.secret_key = "rahasia_banget"

def get_crypto_tool():
	if "user_key" in session:
		return fernet(session["user_key"].encode())
	
	return fernet(b"_JGnUepJSDVSYLdxdc4yohL306GT57y84Qwfig0ahmc=")

def enkrip(text):
	f = get_crypto_tool()
	return f.encrypt(text.encode()).decode()

def dekrip(text):
	f = get_crypto_tool()
	return f.decrypt(text.encode()).decode()

def save_data_worker(data_to_save):
	with open("data.json", "w") as f:
		json.dump(data_to_save, f, indent=4)
	print("[Thread] Data berhasil disimpan aman ke data.json")

def trigger_save():
	thread = threading.Thread(target=save_data_worker, args=(data,))
	thread.start()

# Load data awal
if os.path.exists("data.json"):
	with open("data.json", "r") as read:
		data = json.load(read)
		key = None
else:
	data = {"tesvalid": "", "teks": []}
	key = fernet.generate_key()
	f = fernet(key)
	enkrip_awal = f.encrypt(b"ini valid")
	data["tesvalid"] = enkrip_awal.decode('utf-8')
	with open("data.json", "w") as f:
		json.dump(data, f)

@app.route("/", methods=["GET", "POST"])
def index():
	status = None
	if request.method == "POST":
		try:
			user = request.form["nama"] # Ini password/key bentukan user
			# Cek validitas key yang dimasukkan user
			try_key = fernet(bytes(user, "utf-8"))
			if try_key.decrypt(data["tesvalid"].encode()).decode() == "ini valid":
				status = "login berhasil"
				session["login"] = True
				session["user_key"] = user 
				return redirect("/home/")
			else:
				status = "password salah"
		except Exception as e:
			status = "password salah"
			print(f"Error login: {e}")
            
	if key:
		return render_template("index.html", password=key.decode(), status=status)
	else:
		return render_template("index.html", status=status)

@app.route("/home/", methods=["GET", "POST"])
def home():
	if not session.get("login"):
		return redirect("/")

	# Proses dekripsi di halaman home 
	data_dekrip = {"teks":[]}
	if data["teks"]:
		for i in range(0, len(data["teks"])):
			try:
				decrypted_password = dekrip(data["teks"][i]['password'])
			except Exception:
				decrypted_password = "[Gagal Dekripsi - Key Salah]"

			data_dekrip["teks"].append({
				"username" : data["teks"][i]['username'], 
				"label"    : data["teks"][i]['label'], 
				"password" : decrypted_password,
				"created"  : data["teks"][i]['created'],
			})

	if request.method == "POST":
		label = request.form["label"]
		username = request.form["username"]
		password = request.form["password"]

		tanggal = datetime.datetime.now()
		format_tanggal = tanggal.strftime('%d %B %Y')

		data["teks"].append({
			"username" : username.upper(),
			"label"    : label.upper(),
			"password" : enkrip(password),
			"created"  : format_tanggal
		})
		trigger_save() 
		return redirect("/home/")

	return render_template("home.html", data=data_dekrip)

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/delete/<int:index>")
def hapus(index):
	if not session.get("login"):
		return redirect("/")

	data["teks"].pop(index)
	trigger_save() 
	return redirect("/home/")

@app.route("/edit", methods=["POST"])
def edit_data():
	if not session.get("login"):
		return redirect("/")
        
	idx = int(request.form["index"])
	data["teks"][idx]["label"] = request.form["label"].upper()
	data["teks"][idx]["username"] = request.form["username"]
	data["teks"][idx]["password"] = enkrip(request.form["password"])
    
	trigger_save() 
	return redirect("/home/")

if __name__ == "__main__":
	app.run(debug=True)
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
    
    data["teks"][idx]["label"] = request.form["label"].upper()
    data["teks"][idx]["username"] = request.form["username"]
    data["teks"][idx]["password"] = enkrip(request.form["password"])

    return redirect("/home/")
app.run(debug=True)
