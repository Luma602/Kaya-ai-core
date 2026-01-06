
from flask import Flask, render_template, request, jsonify, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from database import log_chat, init_db
from ai_online import online_ai
from ai_offline import offline_ai
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

login = LoginManager(app)
login.login_view = "login_owner"

USERS = {"owner": os.environ.get("OWNER_PASSWORD", "owner123")}

class User(UserMixin):
    def __init__(self, id): self.id = id

@login.user_loader
def load_user(uid):
    return User(uid) if uid in USERS else None

@app.route("/")
def home():
    return render_template("public.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    text = request.json["text"]
    reply = online_ai(text)
    log_chat("public", text, reply)
    return jsonify({"reply": reply})

@app.route("/owner/login", methods=["GET","POST"])
def login_owner():
    if request.method == "POST":
        if request.form["password"] == USERS["owner"]:
            login_user(User("owner"))
            return redirect("/owner")
    return render_template("login.html")

@app.route("/owner")
@login_required
def owner():
    return render_template("owner.html")

@app.route("/api/owner", methods=["POST"])
@login_required
def owner_chat():
    text = request.json["text"]
    reply = offline_ai(text)
    log_chat("owner", text, reply)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    init_db()
    app.run()
