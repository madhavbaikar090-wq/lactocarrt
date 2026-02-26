from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "lactocart_secret"

# Create DB
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.close()

@app.route('/')
def home():
    return "LactCart is live"

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('users.db')
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password)).fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect("/")
        return "Invalid Login"
    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('users.db')
        conn.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)