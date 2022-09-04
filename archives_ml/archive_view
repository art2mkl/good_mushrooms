from flask import render_template, redirect, url_for, flash, session
import pandas as pd
from app.models.models import db, User, Data
from dotenv import load_dotenv
import os
from app.models.mushroom_viz import Mushroom_viz

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
        raw_df = mushroom.df_to_png(mushroom.df, 'Raw Dataframe', True, 6, 6)

        #charge analyse
        raw_shape = mushroom.data_shape()

        #load object with modified df load in db and drop _id
        df = pd.read_sql_query(db.select(Data), db.engine).drop('_id', axis=1)
        mushroom = Mushroom_viz(df, '_class')

        #charge dataload
        modified_df = mushroom.df_to_png(mushroom.df, 'Modified Dataframe', True, 6, 6)

        #charge sample
        df_sample = mushroom.data_sample()
        df_sample = mushroom.df_to_png(df_sample, 'Dataframe Sample')

        # Plot target repartition
        target = mushroom.look(mushroom.target)
        
        #Get list of features distribution
        print('debut')
        dist_features = [mushroom.look(col) for col in mushroom.X.columns]
        print('fin')

        #Get list of features distribution
        print('debut')
        dist_features_with_hue = [mushroom.look_with_hue(col, '_class') for col in mushroom.X.columns]
        print('fin')

        return render_template(
            'exploration/explore.html', 
            raw_df = raw_df, 
            raw_shape = raw_shape,
            modified_df = modified_df,
            df_sample = df_sample,
            target = target,
            dist_features = dist_features,
            dist_features_with_hue = dist_features_with_hue
            ) 