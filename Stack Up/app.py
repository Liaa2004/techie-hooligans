import firebase_admin
from firebase_admin import db, credentials
from flask import Flask, request, render_template, flash, redirect, url_for

app = Flask(__name__)
error = None
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://techiehooligans-default-rtdb.firebaseio.com/"})

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login" , methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/home" , methods = ["GET", "POST"])
def home():
    user = request.form.get("username")
    path = f"/users/{user}"
    password = request.form.get("password")
    if db.reference(f"{path}/details/password").get() == password:
        return render_template(f"{db.reference(f'{path}/details/accountType').get()}.html", name=db.reference(f"{path}/details/Name").get())
    return render_template("login.html", error="Invalid Credentials")


@app.route("/signup")
def signup():
    global error
    if error != None:
        error, temp = None, error
        return render_template("signup.html", error = temp)
    return render_template("signup.html")


@app.route("/account_created", methods=["POST"])
def account_created():
    global error
    if request.form.get("password") != request.form.get("password1"):
        error = "Passwords do not match"        
    elif request.form.get("username") in db.reference("/users").get():
        error = "User already exists"
    else:
        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        accountType = request.form.get("accountType")
        db.reference(f"/users/{username}/details").set({"Name" : name, "password" : password, "accountType" : accountType})
        return "<h1>User created successfully.</h1>"
    return redirect(url_for("signup"))