from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect('posts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    return render_template("index.html", posts=posts)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form['username']
        pw = request.form['password']
        if user == "member" and pw == "secret":
            session["user"] = user
            return redirect("/upload")
    return render_template("login.html")

@app.route("/upload", methods=["GET","POST"])
def upload():
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        text = request.form["text"]
        file = request.files["image"]

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            conn = get_db()
            conn.execute("INSERT INTO posts (text, image) VALUES (?, ?)", (text, filename))
            conn.commit()

        return redirect("/")

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
