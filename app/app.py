"""
VULNERABLE-LAB : application Flask volontairement vulnérable.
NE JAMAIS DÉPLOYER EN PRODUCTION. Usage pédagogique uniquement.
"""
import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)

# [SAST / Secrets] Clé secrète et identifiants en dur (valeurs factices)
app.config["SECRET_KEY"] = "super-secret-key-123"
DB_PASSWORD = "admin123"
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

DB_PATH = "users.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT)"
    )
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return "VULNERABLE-LAB : essayez /login, /search, /ping, /greet, /file, /fetch, /load"


# [SAST] CWE-89 : injection SQL
@app.route("/login", methods=["POST", "GET"])
def login():
    name = request.values.get("name", "")
    password = request.values.get("password", "")
    query = "SELECT * FROM users WHERE name = '%s' AND password = '%s'" % (name, password)
    row = get_db().execute(query).fetchone()
    return "Bienvenue !" if row else "Echec", 200 if row else 401


# [SAST] CWE-78 : injection de commande
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out


# [SAST / DAST] CWE-79 : XSS réfléchi via SSTI/Jinja non échappé
@app.route("/greet")
def greet():
    name = request.args.get("name", "inconnu")
    return render_template_string("<h1>Bonjour " + name + "</h1>")


# [SAST / DAST] CWE-22 : path traversal
@app.route("/file")
def read_file():
    filename = request.args.get("name", "README.md")
    return send_file(os.path.join("/app/files", filename))


# [SAST] CWE-918 : SSRF
@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    return requests.get(url, verify=False, timeout=5).text


# [SAST] CWE-502 : désérialisation non sûre (pickle + yaml.load)
@app.route("/load", methods=["POST"])
def load():
    kind = request.args.get("type", "yaml")
    data = request.get_data()
    if kind == "pickle":
        return str(pickle.loads(data))
    return str(yaml.load(data, Loader=yaml.Loader))


# [SAST] CWE-327 : hachage faible
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()


if __name__ == "__main__":
    init_db()
    # [SAST] CWE-489 : debug activé + écoute sur toutes les interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)
