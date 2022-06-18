from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Flask Instance
app = Flask(__name__, template_folder='templates')

#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key
app.config['SECRET_KEY'] = "qwertyuiop"
#Initialize database
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create String
    def __repr__(self) :
        return  '<Name %r>' % self.name


#Class userForm
class UserForm(FlaskForm):
    name = StringField("Insert Your Name", validators=[DataRequired()])
    email = StringField("Insert Your Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Class nameForm
class NameForm(FlaskForm):
    name = StringField("Insert Your Name", validators=[DataRequired()])
    # email = StringField("Insert Your Email", validators=[DataRequired()])
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

@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
 
    form = UserForm()
    #Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User Added Succesfully!")
    our_users = Users.query.order_by(Users.date_added)
    
    return render_template("add_user.html",
                           form = form,
                           name = name,
                           our_users = our_users
                           )

# @app.route('/name',methods=['GET','POST'])
# def name():
#     return render_template("name.html")
#     name = None
#     form = NameForm()
    
#     #Validate Form
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data  = ""
#         flash("Form Submitted Successfuly")
        
#     return render_template("name.html",
#                            name = name,
#                            form = form
#                            )

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template("update.html",
                                   form=form,
                                   name_to_update = name_to_update)
        except:
            flash("Error, Try Again!")
            return render_template("update.html",
                                   form=form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                   form=form,
                                   name_to_update = name_to_update)
            
@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    pass

if __name__ == "__main__":
    app.run(debug=True);
