from flask import Flask, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Flask Instance
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = "qwertyuiop"

#Form Class
class NameForm(FlaskForm):
    name = StringField("Insert Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
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


@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NameForm()
    
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data  = ""
        
    return render_template("name.html",
                           name = name,
                           form = form
                           )
    

if __name__ == "__main__":
    app.run(debug=True);