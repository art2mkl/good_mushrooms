from flask import render_template, redirect, url_for, flash, session
import pandas as pd
from app.models import db, User, Data
from dotenv import load_dotenv
import os
from app.helpers import Mushroom_viz

# import the exploration blue print instance
from app.exploration import exploration


@exploration.route('/')
def explore():
    """-------------------------------------------------------------------------------------
Go to Home page

    Parameters :
    None

    Returns :
    redirection to login if no session or index in session

   -------------------------------------------------------------------------------------"""

    if not session:
        flash("access not authorized", "danger")
        return redirect(url_for('main.login'))
    else:

        #load object
        mushroom = Mushroom_viz(pd.read_csv('mushrooms.csv'), 'class')
        
        #load raw df
        raw_df = mushroom.df_to_html(mushroom.df)

        #charge analyse
        raw_shape = mushroom.data_shape()

        #load object with modified df load in db
        df = pd.read_sql_query(db.select(Data), db.engine)
        mushroom = Mushroom_viz(df, '_class')

        #charge dataload
        modified_df = mushroom.df_to_html(mushroom.df)

        #charge sample
        df_sample = mushroom.data_sample()

        # Plot target repartition
        target = mushroom.look(mushroom.target)
        
        #drop _id
        mushroom.X = mushroom.X.drop('_id', axis=1)
        print(mushroom.X.columns)

        #Get list of features distribution
        print('debut')
        dist_features = [mushroom.look(col) for col in mushroom.X.columns]
        print('fin')

        return render_template(
            'exploration/explore.html', 
            raw_df = raw_df, 
            raw_shape = raw_shape,
            modified_df = modified_df,
            df_sample = df_sample,
            target = target,
            dist_features = dist_features
            ) 