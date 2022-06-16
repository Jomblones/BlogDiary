from flask import Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

if __name__ == "__main__":
    app.run(debug=True);