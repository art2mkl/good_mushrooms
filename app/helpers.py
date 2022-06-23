import pandas as pd

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
import base64
from io import BytesIO


class Mushroom_viz():
    
    def __init__(self,df, target):
        """--------------------------------------------------------
        Initialize Object with Data

            Parameters
            df, target

            Returns
            None 
        ---------------------------------------------------------"""
        self.df = df
        self.X = df.drop(target, axis = 1)
        self.y = df[target]
        self.target = target

#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def df_to_html(self,df):
        """--------------------------------------------------------
        Transform tf to html table string

            Parameters
            df

            Returns
            df to html string
        ---------------------------------------------------------"""
        df_tohtml = df.to_html(max_rows = 6, max_cols = 6)

        return df_tohtml
    
#--------------------------------------------------------------------
#--------------------------------------------------------------------

    def data_shape(self):
        """--------------------------------------------------------
        Shows basics infos from dataset

            Parameters
            self

            Returns
            dict with informations
        ---------------------------------------------------------"""
        dict = {
            'nb_lines': self.df.shape[0],
            'nb_cols' : self.df.shape[1],
            'nb_no_null_cells' : self.df.notna().sum().sum(),
            'nb_null_cells' : self.df.isna().sum().sum()
        }
        return dict

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    
    def data_sample(self):
        """--------------------------------------------------------
        Shows samples of features from dataset

            Parameters
            self

            Returns
            df to html string
        ---------------------------------------------------------"""
        samples = []
        for i in self.df.columns:
            samples.append(str(list(self.df[i].head(5))))

        distincts = []
        for i in self.df.columns:
            distincts.append(len(pd.unique(self.df[i])))

        obs = pd.DataFrame({
            'name' : self.df.columns,
            'type':self.df.dtypes,
            'sample':samples,
            'nb_distinct_values': distincts,
            '% nulls':round((self.df.isnull().sum()/len(self.df))*100)   
            })

        return obs.to_html()   
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    
    
    def look(self, target):
        """--------------------------------------------------------
        Shows a distribution graph of target

            Parameters
            target in String

            Returns
            dict with target name and string of buffer img source
        ---------------------------------------------------------"""
        
        fig, ax = plt.subplots(figsize=(5,5))
        plot = sns.countplot(x = self.df[target], color = 'cornflowerblue', ax=ax)
        ax.set_title(f'Distribution of {target}', size=15, weight='bold')
        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)
        ax.bar_label(ax.containers[0])
        xrotation = 0 if len(ax.get_xticks()) < 8 else 45
        ax.tick_params(labelsize=10, labelrotation=xrotation)

        #Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")

        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return {'target' : target, 'source' : f'data:image/png;base64,{data}'}
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    