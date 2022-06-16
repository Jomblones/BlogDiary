from flask import Flask, redirect, render_template, url_for

app = Flask(__name__, template_folder='templates')

@app.route('/')
def toHome():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")
