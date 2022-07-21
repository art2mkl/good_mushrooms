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
import dataframe_image as dfi


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

    def df_to_png(self, df, df_name:str, sample = False, lines:int = 0, columns:int = 0):
        """--------------------------------------------------------
        Transform df to image loaded in buffer memory
            Parameters
            dataframe, sample, nb_lines displayed, nb_column displayed

            Returns
            dict with target name and string of buffer img source
        ---------------------------------------------------------"""

        #Save it to a temporary buffer.
        buf = BytesIO()

        if sample == True:
            df=df.iloc[:lines,:columns]
            df['...'] = '...'
        
        styles = [
            dict( selector="th", props=[
                ("color", "#fff"),
                ("border", "1px solid #333"),
                ("padding", "12px 35px"),
                ("border-collapse", "collapse"),
                ("background", "cornflowerblue"),
                ("text-transform", "uppercase"),
                ("font-size", "20px")
                ]),
            dict(selector="td", props=[(
                "color", "#000"),
                ("border", "1px solid #333"),
                ("padding", "12px 35px"),
                ("border-collapse", "collapse"),
                ("font-size", "20px")
                ]),
            dict(selector="table", 
                props=[
                ("margin" , "25px auto"),
                ("border-collapse" , "collapse"),
                ("border" , "1px solid #333"),
                ("border-bottom" , "2px solid #00cccc"),                                    
                ]),
            dict(selector="caption", props=[("caption-side", "bottom"),("margin", "10px auto")])
        ]
    
        df = df.style.set_table_styles(styles).set_caption(f"Sample of {df_name} (made with pandas)")
     
        dfi.export(df,buf)

        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return {'target' : df_name, 'source' : f'data:image/png;base64,{data}'}   
    
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
            'nb_duplicates': self.df.duplicated().sum(),
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
            df
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

        return obs 
    
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

    def look_with_hue(self, target, hue):
        """--------------------------------------------------------
        Shows a distribution graph of target with hue

            Parameters
            target in String

            Returns
            dict with target name and string of buffer img source
        ---------------------------------------------------------"""
        
        fig, ax = plt.subplots(figsize=(5,5))
        plot = sns.countplot(x = self.df[target], color = 'cornflowerblue', ax=ax, hue=self.df[hue], dodge=True)
        ax.set_title(f'Distribution of {target}', size=15, weight='bold')
        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)
        ax.bar_label(ax.containers[0])
        xrotation = 0 if len(ax.get_xticks()) < 8 else 45
        ax.tick_params(labelsize=10, labelrotation=xrotation)
        ax.legend(loc='center')

        #Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")

        # Embed the result in the html output.
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        return {'target' : target, 'source' : f'data:image/png;base64,{data}', 'hue' : hue}
    
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    