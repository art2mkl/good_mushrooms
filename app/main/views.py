from flask import current_app, render_template, request, redirect, url_for, flash, session
from app.models import db, User
from dotenv import load_dotenv
import os

# import the main blue print instance
from app.main import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/init_db/')
def init_db():

    #Load ENV variables
    load_dotenv('.flaskenv')

    #drop all tables and recreate
    db.drop_all()
    db.create_all()

    # #add 1 user
    db.session.add(User(email=os.getenv('USER_MAIL'), password=os.getenv('USER_PASSWORD'), name=os.getenv('USER_NAME')))
    db.session.commit()

    flash("Database is initialized successfully", "success")

    return redirect(url_for('main.index'))