from flask import current_app, render_template, request, redirect, url_for, flash, session
from app.models import db, User
from dotenv import load_dotenv
import os
from app.main.forms import LoginForm, RegisterForm

# import the main blue print instance
from app.main import main


@main.route('/')
def home():
    if not session:
        return redirect(url_for('main.login'))
    else: 
        return render_template('main/index.html')   

@main.route('/init_db/')
def init_db():

    #Load ENV variables
    load_dotenv('.env')

    #drop all tables and recreate
    db.drop_all()
    db.create_all()

    # #add 1 user
    db.session.add(User(email=os.getenv('USER_MAIL'), password=os.getenv('USER_PASSWORD'), name=os.getenv('USER_NAME')))
    db.session.commit()

    flash("Database is initialized successfully", "success")

    return redirect(url_for('main.index'))

@main.route('/test')
def test():
    return 'Test Serveur'

@main.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate(): 
            flash("Successfully logged in as %s." % form.user.email, "success")
            return redirect(url_for('main.home'))
    else:
        form = LoginForm()
    return render_template("main/login.html", form=form)

@main.route('/logout/')
def logout():
    session.pop('user','')
    session.pop('id','')

    flash("Successfully unlogged", "warning")
    return redirect(url_for('main.login'))

@main.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():

            if User.exists(form.email.data):
                flash(f"User {form.email.data} already exists !", 'danger')
                return render_template('main/register.html', form=form)

            else:
                user= User(form.name.data, form.email.data, form.password.data)
                db.session.add(user)
                db.session.commit()

                flash(f"User { user.name } is created successfully", 'success')

                #Load session
                User.load_session(user.email)
                return redirect(url_for('main.home'))

    else:
        form = RegisterForm()

    return render_template('main/register.html', form=form)

@main.route('/profil/', methods=['GET', 'POST'])
def profil():
    if not session:
        return redirect(url_for('main.login'))

    else:

        user = User.query.filter(User.id == session['id']).first_or_404()

        if request.method == 'POST':
            form = RegisterForm(request.form, obj=user)
            if form.validate():
                
                user.name=form.name.data
                user.role=form.role.data
                db.session.commit()

                #Load session
                User.load_session(user.email)

                flash(f"Entry {user.name} is updated successfully", 'success')
                return redirect(url_for('main.home'))

        else:
            form = RegisterForm(obj=user)
            
        return render_template('main/profil.html', form=form)