from flask import render_template, redirect, url_for, flash, session
import pandas as pd
from app.models.models import db, User, Data
from dotenv import load_dotenv
import os
from app.models.mushroom_ml import Mushroom_ml

# import the basic blue print instance
from app.basic import basic


@basic.route('/')
def basic():
    """-------------------------------------------------------------------------------------
Go to Basic ML page

    Parameters :
    None

    Returns :
    redirection to login if no session or basic ml if session

   -------------------------------------------------------------------------------------"""

    if not session:
        flash("access not authorized", "danger")
        return redirect(url_for('main.login'))
    else:

        #load object with modified df load in db
        df = pd.read_sql_query(db.select(Data), db.engine)
        mushroom = Mushroom_ml(df, '_class')
        display_df=[]

        #charge dataload
        display_df.append(mushroom.df_to_html(df, 'Dataframe', 6, 6))

        #drop index
        new_df = mushroom.df_drop_cols(df, '_id')       
        display_df.append(mushroom.df_to_html(new_df, 'Dataframe', 6, 6))

        print(mushroom.X.columns)
        return render_template(
            'basic/basic.html',
            display_df=display_df
            ) 