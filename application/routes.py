from application import app,db
from flask import render_template,flash,redirect,url_for,request
from application.forms import LoginForm,RegistrationForm,LoadForm
from flask_login import login_required,current_user,login_user,logout_user
from werkzeug.urls import url_parse
from application.models import User,Devices


@app.route('/index',methods=['GET', 'POST'])
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
]
    return render_template('index.html',title = 'Home', posts = posts)



@app.route('/login',methods = ["GET","POST"])
def login():
    if current_user.is_authenticated:
       return redirect('/index')
    my_form = LoginForm()
    load_form = LoadForm()
    if my_form.validate_on_submit():
       u = User.query.filter_by(username = my_form.username.data).first()
       if u is None or not u.check_password(password = my_form.password.data):
          flash("Invalid username or Incorrect password")
          return redirect('/login')
       login_user(u,remember = my_form.remember_me.data) 
       next_page = request.args.get('next')
       #if not is_safe_url(next):
          #return flask.abort(400)
       if not next_page or url_parse(next_page).netloc != '':
           next_page = url_for('index')
       flash("Login is successful for the user {} and remember me {}".format(my_form.username.data,my_form.remember_me.data))
       return redirect(next_page)
    return render_template('login.html',Title = 'Sign In',form = my_form)



@app.route('/register' , methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
       return redirect('/index')
    my_form = RegistrationForm()
    if my_form.validate_on_submit():
       u = User(username=my_form.username.data,email=my_form.email.data)
       u.set_password(my_form.password.data)
       db.session.add(u)
       db.session.commit()
       flash("Congratulations you have Registered in successfully")
       return redirect(url_for('login'))
    return render_template('register.html',title = 'Register',form = my_form) 


@app.route('/load',methods = ['GET','POST'])
@login_required
def load():
    load_form = LoadForm()
    if load_form.validate_on_submit():
       print(current_user.id)
       l =  Devices(id=load_form.id.data,name=load_form.name.data,power=load_form.power.data,user_id = current_user.id)
       db.session.add(l)
       db.session.commit()
       flash("Congratulations your load was added")
       return render_template('index.html',title = 'Load_details',form = load_form)
    return render_template('loads.html',title = 'Load_details',form = load_form) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')
