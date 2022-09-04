from flask import render_template, redirect, url_for, flash, session

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

        return render_template(
            'exploration/explore.html'
            ) 