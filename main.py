from flask import Flask, render_template, request, redirect, url_for, make_response
from model import User, db
import hashlib, uuid
app = Flask(__name__)

db.create_all() # erstellt neue Datenbank Tabelle(n)

@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
    else:
        user = None
    #print(user.name)
    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    print(hashed_pw)

    #neues Objekt von Typ User (Model)
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, password=hashed_pw)
        db.add(user)
        db.commit()
    if hashed_pw != user.password:
        return  "Wrong Password! Try again"
    elif hashed_pw == user.password:
        session_token = str(uuid.uuid4())
        user.session_token = session_token
        db.add(user)
        db.commit()
        #cookie
        response = make_response(redirect(url_for('index')))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')
        return response

if __name__ == '__main__':
    app.run()