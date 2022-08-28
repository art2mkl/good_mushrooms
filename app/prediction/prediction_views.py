from flask import render_template, redirect, url_for, flash, session, jsonify
import pandas as pd
from app.models.models import db, User, Data, Ml
from dotenv import load_dotenv
import os
from joblib import load

# import the basic blue print instance
from app.prediction import prediction


@prediction.route('/')
def make_prediction():
    """-------------------------------------------------------------------------------------
Go to PREDICTION page

    Parameters :
    None

    Returns :
    redirection to login if no session or basic ml if session

   -------------------------------------------------------------------------------------"""

    if not session:
        flash("access not authorized", "danger")
        return redirect(url_for('main.login'))
    else:

        
        return render_template(
            'prediction/prediction.html'
            ) 


# @prediction.route('/predict/<sendmodel>/<_odor>/<_habitat>/<_cap_color>/<_bruises>/')
# def predict(sendmodel, _odor, _habitat, _cap_color, _bruises):
#     """-------------------------------------------------------------------------------------
#     Load model and Make PREDICTION page

#     Parameters :
#     sendmodel,
#     _odor,
#     _habitat,
#     _cap_color,
#     _bruises

#     Returns :
#     json of prediction

#    -------------------------------------------------------------------------------------"""
   
#     return None

@prediction.route('/choosemodel/')
def choosemodel():
    """-------------------------------------------------------------------------------------
    Select models in db

    Parameters :
    none

    Returns :
    string of models

   -------------------------------------------------------------------------------------"""
   
    models_array=[]
    for model in Ml.query.filter(Ml.display==True).all():
        model_obj={}
        model_obj['id']=model.id
        model_obj['name']=model.name
        model_obj['model']=model.model
        model_obj['cols']=model.cols
        model_obj['accuracy']=model.accuracy
        model_obj['precision']=model.precision
        model_obj['path']=model.path
        models_array.append(model_obj)
        


    return jsonify({'models': models_array})