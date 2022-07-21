import pandas as pd
import os
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="white", rc={
        "axes.edgecolor": "black",
        "ytick.color":"white",
        'axes.spines.left': False,      
        'axes.spines.right': False,
        'axes.spines.top': False})

#ml process
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

#preprocessing
from sklearn.preprocessing import StandardScaler, OneHotEncoder

#models
from sklearn import tree
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifierCV
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

#metrics
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score

#save
from joblib import dump, load


class Mushroom_ml():
    
    
    def __init__(self,df, target):
        """--------------------------------------------------------
        Initialize Object with Data

            Parameters
            df, target

            Returns
            None 
        ---------------------------------------------------------"""
        self.df = df
        self.X = df.drop([target,'_id'], axis = 1)
        self.y = df[target]
        self.target = target

#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def df_to_html(self, df, df_name:str, lines:int = 5, columns:int = 5):
        """--------------------------------------------------------
        Transform df to HTML string
            Parameters
            dataframe, sample, nb_lines displayed, nb_column displayed

            Returns
            dict with target name and string of buffer img source
        ---------------------------------------------------------"""

        return df.to_html(max_rows=lines, max_cols=columns) 
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def df_drop_cols(self, df, cols):
        """--------------------------------------------------------
        drop cols in df from list and update df
            Parameters
            dataframe, columns_names to drop

            Returns
            df updated
        ---------------------------------------------------------"""

        df=df.drop(cols, axis=1)

        return df 
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def train_test_split(self, X, y):
        """--------------------------------------------------------
        separate dataset in training and testing sets

            Parameters
            X(features), y(target)

            Returns
            None
        ---------------------------------------------------------"""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        return None
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def test_models(self, X, y):
        """--------------------------------------------------------
        Test list of models and give mean accuracy after a cross validation
            
            Parameters
            dataframe, columns_names to drop

            Returns
            df updated
        ---------------------------------------------------------"""

        list_models = [
            LogisticRegression(),
            SGDClassifier(),  
            LinearSVC(),
            KNeighborsClassifier(n_neighbors=10),
            StackingClassifier([
                    ('model_1', LogisticRegression()),('model_2', LogisticRegression())
                ], final_estimator=LogisticRegression()),
            AdaBoostClassifier(),
            GradientBoostingClassifier(),
            RandomForestClassifier(n_estimators=10),
        ]

        for model in list_models:
            final_model = make_pipeline(OneHotEncoder(handle_unknown='ignore'), model)
            print("\n" + f"model : {model} => {cross_val_score(final_model, X, y, cv).mean()}")

        return None
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def training_models(self, X, y, model):
        """--------------------------------------------------------
        Test list of models and give mean accuracy after a cross validation
            
            Parameters
            dataframe, columns_names to drop

            Returns
            df updated
        ---------------------------------------------------------"""

        list_models = [
            LogisticRegression(),
            SGDClassifier(),  
            LinearSVC(),
            KNeighborsClassifier(n_neighbors=10),
            StackingClassifier([
                    ('model_1', LogisticRegression()),('model_2', LogisticRegression())
                ], final_estimator=LogisticRegression()),
            AdaBoostClassifier(),
            GradientBoostingClassifier(),
            RandomForestClassifier(n_estimators=10),
        ]

        for model in list_models:
            final_model = make_pipeline(OneHotEncoder(handle_unknown='ignore'), model)
            print("\n" + f"model : {model} => {cross_val_score(final_model, X, y, cv).mean()}")

        return None
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------



