from flask import render_template, redirect, url_for, flash, request, session
import pandas as pd
from numpy import genfromtxt
from app.models.models import db, User, Data, Ml
import shutil
from dotenv import load_dotenv
import os
from app.main.forms import LoginForm, RegisterForm

# import the main blue print instance
from app.main import main

def del_folder(folder):
    """-------------------------------------------------------------------------------------
Delete <folder> and create it again

    Parameters :
    folder

    Returns :
    None
   --------------------------------------------------------------------------------------"""

    try:
        shutil.rmtree(folder)
    except OSError as e:
        print("initialisation du repertoire")
        # print(f"Error:{ e.strerror}")

    # créé le repertoire <folder>
    os.makedirs(folder, exist_ok=True)

@main.route('/')
def home():
    """-------------------------------------------------------------------------------------
Go to Home page

    Parameters :
    None

    Returns :
    redirection to login if no session or index in session

   -------------------------------------------------------------------------------------"""

    if not session:
        return redirect(url_for('main.login'))
    else: 
        return render_template('main/index.html')   


@main.route('/init_db/')
def init_db():
    """-------------------------------------------------------------------------------------
init db, drop all tables and init tables

    Parameters :
    None

    Returns :
    redirection to route home

   -------------------------------------------------------------------------------------"""
    #Load ENV variables
    load_dotenv('.env')

    #drop all tables and recreate
    db.drop_all()
    db.create_all()

    # #add 1 user
    db.session.add(User(email=os.getenv('USER_MAIL'), password=os.getenv('USER_PASSWORD'), name=os.getenv('USER_NAME')))
    db.session.commit()

    #load .csv on data
    load_csv()

    #del models folders
    del_folder('app/models/load_models')  

    flash("Database is initialized successfully", "success")
    return redirect(url_for('main.home'))


@main.route('/test')
def test():
    """-------------------------------------------------------------------------------------
route for test function with pytest

    Parameters :
    None

    Returns :
    string to compare
   -------------------------------------------------------------------------------------"""
    return 'Test Serveur'


@main.route("/login/", methods=["GET", "POST"])
def login():
    """-------------------------------------------------------------------------------------
route for login user

    Parameters :
    None

    Returns :
    render template login.html or redirect home if form is validated 
    -------------------------------------------------------------------------------------"""
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
    """-------------------------------------------------------------------------------------
route for logout

    Parameters :
    None

    Returns :
    redirect home ans delete session variables
    -------------------------------------------------------------------------------------"""
    session.pop('user','')
    session.pop('id','')

    flash("Successfully unlogged", "warning")
    return redirect(url_for('main.login'))


@main.route('/register/', methods=['GET', 'POST'])
def register():
    """-------------------------------------------------------------------------------------
route for register user

    Parameters :
    None

    Returns :
    render template register.html or redirect home if form is validated 
    -------------------------------------------------------------------------------------"""

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

@main.route('/load_csv/', methods=['GET'])
def load_csv():
    """-------------------------------------------------------------------------------------
load csv data in dataframe, clean it and load it in db

    Parameters :
    None

    Returns :
    String
    -------------------------------------------------------------------------------------"""
    #load csv_file in df
    df = pd.read_csv('mushrooms.csv')

    #change features in full strings
    df = change_features_in_full_strings(df)

    #persist in db
    for row, col in df.iterrows():

        new_data = Data(
            _class = col[0],
            _cap_shape = col[1],
            _cap_surface = col[2],
            _cap_color = col[3],
            _bruises = col[4],
            _odor = col[5],
            _gill_attachment = col[6],
            _gill_spacing = col[7],
            _gill_size =  col[8],
            _gill_color = col[9],
            _stalk_shape = col[10],
            _stalk_root = col[11],
            _stalk_surface_above_ring = col[12],
            _stalk_surface_below_ring = col[13],
            _stalk_color_above_ring = col[14],
            _stalk_color_below_ring = col[15],
            _veil_type = col[16],
            _veil_color = col[17],
            _ring_number = col[18],
            _ring_type = col[19],
            _spore_print_color = col[20],
            _population = col[21],
            _habitat = col[22],
        )
        db.session.add(new_data)
    db.session.commit()
         
    return 'Data is loaded'

def change_features_in_full_strings(df):
    """-------------------------------------------------------------------------------------
Transform initial feature string in full feature string in dataframe

    Parameters :
    dataframe

    Returns :
    dataframe transformed
    -------------------------------------------------------------------------------------"""

    #define dict
    class_dict = {'e': 'edible', 'p': 'poisoned'}
    cap_shape_dict = {'b' : 'bell', 'c' : 'conical', 'x':'convex', 'f':'flat', 'k' : 'knobbed', 's' : 'sunken'}
    cap_surface_dict = {'f' : 'fibrous', 'g' : 'grooves', 'y' : 'scaly', 's' : 'smooth'}
    cap_color_dict = {'n' : 'brown', 'b' : 'buff', 'c' : 'cinnamon', 'g' : 'gray', 'r' : 'green', 'p' : 'pink', 'u' : 'purple', 'e' : 'red', 'w' : 'white', 'y' : 'yellow'}
    bruises_dict = { 't' : 'bruises', 'f' : 'no' }
    odor_dict = {'a' : 'almond', 'l' : 'anise', 'c' : 'creosote', 'y' : 'fishy', 'f' : 'foul', 'm' : 'musty', 'n' : 'none', 'p' : 'pungent', 's' : 'spicy'} 
    gill_attachment_dict = {'a' : 'attached', 'd' : 'descending', 'f' : 'free', 'n' : 'notched'}
    gill_spacing_dict = {'c' : 'close', 'w' : 'crowded', 'd' : 'distant'}
    gill_size_dict = {'b' : 'broad', 'n' : 'narrow'}
    gill_color_dict = { 'k' :'black', 'n' : 'brown', 'b' : 'buff', 'h' : 'chocolate', 'g' : 'gray', 'r' : 'green', 'o' : 'orange', 'p' : 'pink', 'u' : 'purple', 'e' : 'red', 'w' : 'white', 'y' : 'yellow'}
    stalk_shape_dict = {'e' : 'enlarging', 't' : 'tapering'}
    stalk_root_dict = {'b' : 'bulbous', 'c' : 'club', 'u' : 'cup', 'e' : 'equal', 'z' : 'rhizomorphs', 'r' : 'rooted', '?' : 'missing'}
    stalk_surface_above_ring_dict = {'f' : 'fibrous', 'y' : 'scaly', 'k' : 'silky', 's' : 'smooth'}
    stalk_surface_below_ring_dict = { 'f' : 'fibrous', 'y' : 'scaly', 'k' : 'silky', 's' : 'smooth'}
    stalk_color_above_ring_dict = {'n' : 'brown', 'b' : 'buff', 'c' : 'cinnamon', 'g' : 'gray', 'o' : 'orange', 'p' : 'pink','e' : 'red', 'w' : 'white', 'y' : 'yellow'}
    stalk_color_below_ring_dict = {'n' : 'brown', 'b' : 'buff', 'c' : 'cinnamon', 'g' : 'gray', 'o' : 'orange', 'p' : 'pink','e' : 'red', 'w' : 'white', 'y' : 'yellow'}
    veil_type_dict = {'p' : 'partial', 'u' : 'universal'}
    veil_color_dict = {'n' : 'brown', 'o' : 'orange', 'w' : 'white', 'y' : 'yellow'}
    ring_number_dict = {'n' : 'none', 'o' : 'one', 't' :'two'}
    ring_type_dict = {'c' : 'cobwebby', 'e' : 'evanescent', 'f' : 'flaring', 'l' : 'large', 'n' :'none', 'p' : 'pendant', 's' : 'sheathing', 'z' : 'zone'}
    spore_print_color_dict = {'k' :'black', 'n' : 'brown', 'b' :'buff', 'h' : 'chocolate', 'r' : 'green', 'o' : 'orange', 'u' : 'purple', 'w' :'white', 'y' : 'yellow'}
    population_dict = {'a' : 'abundant', 'c' : 'clustered', 'n' : 'numerous', 's' : 'scattered', 'v' : 'several', 'y' : 'solitary'}
    habitat_dict = {'g' : 'grasses', 'l' : 'leaves', 'm' : 'meadows', 'p' : 'paths', 'u' : 'urban', 'w' : 'waste', 'd' : 'woods'}

    #change features in df
    df['class'] = df['class'].map(class_dict)
    df['cap-shape'] = df['cap-shape'].map(cap_shape_dict)
    df['cap-surface'] = df['cap-surface'].map(cap_surface_dict)
    df['cap-color'] = df['cap-color'].map(cap_color_dict)
    df['bruises'] = df['bruises'].map(bruises_dict)
    df['odor'] = df['odor'].map(odor_dict)
    df['gill-attachment'] = df['gill-attachment'].map(gill_attachment_dict)
    df['gill-spacing'] = df['gill-spacing'].map(gill_spacing_dict)
    df['gill-size'] = df['gill-size'].map(gill_size_dict)
    df['gill-color'] = df['gill-color'].map(gill_color_dict)
    df['stalk-shape'] = df['stalk-shape'].map(stalk_shape_dict)
    df['stalk-root'] = df['stalk-root'].map(stalk_root_dict)
    df['stalk-surface-above-ring'] = df['stalk-surface-above-ring'].map(stalk_surface_above_ring_dict)
    df['stalk-surface-below-ring'] = df['stalk-surface-below-ring'].map(stalk_surface_below_ring_dict)
    df['stalk-color-above-ring'] = df['stalk-color-above-ring'].map(stalk_color_above_ring_dict)
    df['stalk-color-below-ring'] = df['stalk-color-below-ring'].map(stalk_color_below_ring_dict)
    df['veil-type'] = df['veil-type'].map(veil_type_dict)
    df['veil-color'] = df['veil-color'].map(veil_color_dict)
    df['ring-number'] = df['ring-number'].map(ring_number_dict)
    df['ring-type'] = df['ring-type'].map(ring_type_dict)
    df['spore-print-color'] = df['spore-print-color'].map(spore_print_color_dict)
    df['population'] = df['population'].map(population_dict)
    df['habitat'] = df['habitat'].map(habitat_dict)

    return df


