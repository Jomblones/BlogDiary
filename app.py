from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
from flask_migrate import Migrate
import os

#Flask Instance
app = Flask(__name__, template_folder='templates')

#Add database

# LOCAL DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# PostgreSQL HEROKU m.farhanshihab11@gmail.com - diaryblog2112
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uyuozckgxinllx:fdeeed898474fb989519bd58ebef745c64400e122ef4b7563742786ae9a8bd30@ec2-3-224-164-189.compute-1.amazonaws.com:5432/d6372ho6i6ii9u'

#Secret Key
app.config['SECRET_KEY'] = "qwertyuiop"

#Initialize database
db = SQLAlchemy(app)

#db migration
migrate = Migrate(app,db) 

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create String
    def __repr__(self) :
        return  '<Name %r>' % self.name

#Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

#Class Posts Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author =StringField("Author", validators=[DataRequired()])
    slug =StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
    
# HOMEPAGE
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", menu="home")

# ABOUT PAGE
@app.route('/about')
def about():
    return render_template("about.html", menu="about")

# USER PROFILE PAGE
@app.route('/profile')
def profile():
    return render_template("profile.html",  menu="profile")

# ADD USER
@app.route('/user/add' ,methods=['GET','POST'])
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
                           our_users = our_users,
                           menu="add_user"
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
                                   name_to_update = name_to_update,
                                   id=id)
            
@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    
    try : 
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form = form,name = name,our_users = our_users)

    except:
        flash("User not found")
        return render_template("add_user.html", form = form,name = name,our_users = our_users)
   
# CRUD BLOG  
#Create
@app.route('/add-post', methods=['GET','POST'])
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Posts(title=form.title.data, 
                     content=form.content.data, 
                     author=form.author.data, 
                     slug=form.slug.data
                     )
        
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        
        #add post data to database
        db.session.add(post)
        db.session.commit()
        
        #Return message
        flash("Blog Post Submitted Successfully")

    #Redirect
    return render_template("add_post.html", form=form, menu="add_post")

#Read many posts
@app.route('/posts')
def posts():
    
    #all the posts from DB
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts, menu="posts")

#Read one post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post, menu="posts")

#Update
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        
        #Update to DB
        db.session.add(post)
        db.session.commit()
        
        #message
        flash("Post Updated")
        return redirect(url_for('post', id=post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    
    return render_template("edit_post.html", form=form)

#Delete
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        
        #Flash message
        flash("Post Deleted") 
        
        #Grab All posts
        posts = Posts.query.order_by(Posts.date_posted)        
        return render_template("posts.html", posts=posts)        
    
    except:
        #Error message
        flash("Problem Deleting Post")
        
        #Grab All posts
        posts = Posts.query.order_by(Posts.date_posted)        
        return render_template("posts.html", posts=posts)      

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(505)
def internal_server_error(e):
    return render_template("505.html")

if __name__ == "__main__":
    app.run(debug=True);
