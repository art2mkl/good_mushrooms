import pandas as pd
import os
import json
import time
from urllib.parse import urlparse
import sqlite3

import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns
sns.set_theme(style="white", rc={
        "axes.edgecolor": "black",
        "ytick.color":"black",
        'axes.spines.left': False,      
        'axes.spines.right': False,
        'axes.spines.top': False})

#ml process
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, validation_curve, learning_curve
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

#preprocessing
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

#models
import graphviz
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree, export_graphviz
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression, RidgeClassifierCV
from sklearn.ensemble import StackingClassifier, RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier

#metrics
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, make_scorer, confusion_matrix, ConfusionMatrixDisplay

#save
from joblib import dump, load

import mlflow
import mlflow.sklearn


class Mushroom_ml():
    
    
    def __init__(self,df, target, conn):
        """--------------------------------------------------------
        Initialize Object with Data

            Parameters
            df, target, conn

            Returns
            None 
        ---------------------------------------------------------"""
        self.df = df
        self.X = df.drop(target, axis = 1)
        self.y = df[target]
        self.target = target
        self.list_models = [
            LogisticRegression(),
            SGDClassifier(),
            RidgeClassifierCV(),
            LinearSVC(),
            KNeighborsClassifier(),
            DecisionTreeClassifier(),
            StackingClassifier([
                    ('model_1', KNeighborsClassifier(n_neighbors=10)),('model_2', RandomForestClassifier())
                ], final_estimator=DecisionTreeClassifier()),
            AdaBoostClassifier(),
            GradientBoostingClassifier(),
            RandomForestClassifier(n_estimators=10)
        ]
        self.precision_scorer = make_scorer(self.score_precision, greater_is_better = True)
        self.conn = conn
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

    def score_precision(self, y, y_pred):
        """--------------------------------------------------------
        Define function precision in order to be used with a make_scorer function
        included precision label target("enible")

        Parameters
        y and y_pred

        Returns
        precision score
        ---------------------------------------------------------"""
        return precision_score(y, y_pred, average = "binary", pos_label="edible")
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------

    def train_test_split(self, X, y):
        """--------------------------------------------------------
        separate dataset in training and testing sets

            Parameters
            X(features), y(target)

            Returns
            datasets: X_train, X_test, y_train, y_test
        ---------------------------------------------------------"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        return X_train, X_test, y_train, y_test
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def test_models(self, list_models='default', encoder=OneHotEncoder(handle_unknown='ignore'), scoring='default', show=False):
        """--------------------------------------------------------
        Test list of models and give mean accuracy after a cross validation
            
            Parameters
            list of models, Encoder, scoring

            Returns
            String of
        ---------------------------------------------------------"""
        if list_models == 'default':
            list_models=self.list_models
            
        if scoring == 'default':
            scoring = self.precision_scorer
            
        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)
        
        cat = X_train.select_dtypes(exclude = [np.number]).columns
        transformer = make_column_transformer((encoder, cat))
            
        final_string=""
        for model in list_models:
            
            final_model = make_pipeline(transformer, model)
            string=f"model : {model} => {cross_val_score(final_model, X_train, y_train, cv=4, scoring=scoring).mean()}"
            
            if show:
                print(string)
                
            final_string+= ("\n" + string)
            

        return final_string
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def score_model(self, sendmodel=DecisionTreeClassifier(), encoder=OneHotEncoder(handle_unknown='ignore'), display=True):
        """--------------------------------------------------------
        Train a Model and Score Metrics. Add Monitoring parameters and launch save models

            Parameters
            Model, Encoder, Display

            Returns
            String of
        ---------------------------------------------------------"""

        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)
        
        cat = X_train.select_dtypes(exclude = [np.number]).columns
        transformer = make_column_transformer((encoder, cat))
        
        with mlflow.start_run():
            model = make_pipeline(transformer, sendmodel)
            self.fit_model = model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            precision=precision_score(y_test, y_pred, average = "binary", pos_label="edible")
            accuracy=accuracy_score(y_test, y_pred)
            
            mlflow.log_param("cols", ('||').join(self.X.columns))
            mlflow.log_param("parameters", json.dumps(self.fit_model.steps[1][1].get_params()))
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            
 
                            
        results = [f'accuracy : {accuracy}',
        f'precision : {precision}',
        ]
        for result in results:
            print(result)

        listing = list(y_test.unique())
        listing.sort()
        cm = confusion_matrix(y_test, y_pred, labels=listing)
        fig, ax = plt.subplots(figsize=(8,6))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=listing, )
        disp.plot(cmap=plt.cm.Blues, ax=ax)
        fig.suptitle(f'{sendmodel} Confusion matrix', fontweight='bold', fontsize=20);
        plt.show()
             
        #create in db
        name_model=f'{str(sendmodel)}_{int(time.time())}'
        ml_path=f'/models/load_models/{name_model}'
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO ml(
        name,
        cols,
        model,
        parameters,
        accuracy,
        precision,
        path,
        display) 
        VALUES (?,?,?,?,?,?,?,?)
        """,(
            f'{str(sendmodel)}_{int(time.time())}',
            ('||').join(self.X.columns),
            str(sendmodel),
            json.dumps(self.fit_model.steps[1][1].get_params()),
            float(accuracy),
            float(precision),
            ml_path,
            display         
        ))

        self.conn.commit()
        self.save_model(sendmodel, encoder, ml_path)
        

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    
    
    
    def save_model(self, sendmodel, encoder, ml_path):
        """--------------------------------------------------------
        Create fit_model with full X and y parameters and dump model 

            Parameters
            Model
            Encoder
            ml_path

            Returns
            String
        ---------------------------------------------------------"""
                
        model = make_pipeline(encoder, sendmodel)
        full_model = model.fit(self.X, self.y)
        
        dump(full_model, f'app/{ml_path}')       
        
        return 'Save Model Successfully'
        
    
    def features_importances(self, encoder=OneHotEncoder()):
        """--------------------------------------------------------
        Train a Model of RandomForestClassificator and catch predict important_features

            Parameters
            Encoder

            Returns
            Dataframe
        ---------------------------------------------------------"""
        
        #split
        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)

        #define model and encode
        sendmodel=DecisionTreeClassifier()
        
        cat = X_train.select_dtypes(exclude = [np.number]).columns
        transformer = make_column_transformer((encoder, cat))
        
        model = make_pipeline(transformer, sendmodel)
                
        #fit
        fit_model = model.fit(X_train, y_train)
        

        #create fi(dataframe) with features importances of encoding
        fi = pd.DataFrame(list(zip(fit_model.steps[0][1].get_feature_names_out(),
                               fit_model.steps[1][1].feature_importances_)))

        sumdf=pd.DataFrame([[]])
        for col in list(fit_model.steps[0][1].feature_names_in_):
            somme=[]
            resultat=0

            for i in range(len(fi)):

                if col in fi.iloc[i][0]:
                    somme.append(pow((fi.iloc[i][1]), 2))
                    resultat=sum(somme)

                sumdf[col]=np.sqrt(resultat)

        sumdf = sumdf.T
        sumdf.columns = ['feature_importance']
        sumdf['name']=sumdf.index
        sumdf.sort_values(by = 'feature_importance', ascending = False, inplace=True)
        
        fig, ax = plt.subplots(figsize=(7, 7))
        
        plot = sns.barplot(x='feature_importance', y='name', data=sumdf, color="r", ax=ax, orient='h')
        plt.show()
        
        return sumdf
    
    #--------------------------------------------------------------------
    #-------------------------------------------------------------------- 
    
    
    def feature_selection(self, list_val_features=[], sendmodel=DecisionTreeClassifier(), plot_df=False):
        """--------------------------------------------------------
        Evaluate witch feature have the better score and plot results

            Parameters
            sendmodel, list of validate other features

            Returns
            dataset
        ---------------------------------------------------------"""
    
        liste = self.df.drop(['_class'] + list_val_features, axis=1).columns

        results_test_models = []
        for col in liste:
            df_test = Mushroom_ml(self.df[['_class', col] + list_val_features], '_class', self.conn)
            results_test_models.append(float((df_test.test_models([DecisionTreeClassifier()])).split(' => ')[1]))

        df_results = pd.DataFrame({'feature':liste, 'results':results_test_models}).sort_values(by = 'results', ascending = False)
        if plot_df:
            fig, ax = plt.subplots(figsize=(7, 7))

            plot = sns.barplot(x='results', y='feature', data=df_results, color="r", ax=ax, orient='h')
            plt.show()
            
        return df_results
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    
    def tree_vis(self, sendmodel=DecisionTreeClassifier(), encoder=OneHotEncoder()):
        """--------------------------------------------------------
        Train a Model of DecisionTreeClassifier and viz decision tree of features

            Parameters
            Encoder

            Returns
            graphique in .dot format
        ---------------------------------------------------------"""
        
        #split
        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)
              
        #model = make_pipeline(transformer, sendmodel)
        preprocessing=encoder.fit_transform(X_train)

        #fit
        tree_ml = sendmodel.fit(preprocessing, y_train)

        features = encoder.get_feature_names_out()
        
        dot_data = export_graphviz(tree_ml, out_file=None, 
                                        feature_names=features,  
                                        class_names=tree_ml.classes_,  
                                        filled=True, rounded=True,  
                                        special_characters=True)
        graph = graphviz.Source(dot_data)
        self.text_tree = export_text(tree_ml, feature_names=list(features))

        return graph
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    
       
    def grid_model(self, model, params, scoring='default'):
        """--------------------------------------------------------
        Evaluate better params for a model scoring send it

            Parameters
            model
            params
            scoring

            Returns
            String with best params
        ---------------------------------------------------------"""
        
        if scoring == 'default':
            scoring = {
                "precision_score": self.precision_scorer,
                "accuracy": "accuracy"
            }
        
        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)

        #define model and encode
        encoder=OneHotEncoder()

        #encode
        preprocessing = encoder.fit_transform(X_train)

        # Instantiate the RandomizedSearchCV object: tree_cv
        model_cv = GridSearchCV(model, params, cv=5, scoring = scoring, refit="precision_score")

        # Fit it to the data
        model_cv.fit(preprocessing,y_train)

        # Print the tuned parameters and score
        print("Tuned Decision Tree Parameters: {}".format(model_cv.best_params_))
        print("Best score is {}".format(model_cv.best_score_))
        
        return model_cv.best_params_
    
    #--------------------------------------------------------------------
    #-------------------------------------------------------------------- 
    
    def learning_graph(self, sendmodel=DecisionTreeClassifier(), encoder=OneHotEncoder()):

        """--------------------------------------------------------
        Graph learning curve for better sample of records

        Parameters
        model
        encoder

        Returns
        None
        ---------------------------------------------------------"""

        #split
        X_train, X_test, y_train, y_test = self.train_test_split(self.X, self.y)

        #encode
        preprocessing = encoder.fit_transform(X_train)          

        N, train_score, val_score = learning_curve(sendmodel,
                                                   preprocessing,
                                                   y_train,
                                                   train_sizes = np.linspace(0.2, 1.0, 10),
                                                   cv = 5)

        plt.plot(N, train_score.mean(axis = 1), label = 'train')
        plt.plot(N, val_score.mean(axis = 1), label = 'validation')
        plt.xlabel('train_sizes')

        plt.title(f"Learning Curve of accuracy with {sendmodel}", size=15, weight='bold' )
       
        plt.legend()

        return None
            
    #--------------------------------------------------------------------
    #-------------------------------------------------------------------- 