import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


df=pd.read_csv('medical_examination.csv')

#Adding overweight column
df['height']=df['height']/100
df["BMI"]=df['weight']/(df['height']**2)


# Add Overweight Column (1 if BMI > 25, else 0)
df["Overweight"]=(df["BMI"]>25).astype(int)


#Normalizing data(0 always good and 1 always bad)
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

#Function to draw a categorical plot
def draw_cat_plot():
    categorical_columns = ["cholesterol", "gluc", "smoke", "alco", "active","Overweight"]
    
    # Convert data into long format for categorical plotting
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=categorical_columns,var_name="variable",value_name="value")

    cat_plot=sns.catplot(
        x="variable",  # Categorical feature names on X-axis
        hue="value", # Different colors for each category
        col="cardio",# Separate plots for cardio (0 and 1)
        kind="count",# Count plot
        data=df_cat
    )
    fig=cat_plot.figure
    fig.savefig('catplot.png')

    return cat_plot
draw_cat_plot()


#function to draw a heatmap
def draw_heat_map():
    #filtering the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
                 (df['height'] >= df['height'].quantile(0.025)) & 
                 (df['height'] <= df['height'].quantile(0.975)) & 
                 (df['weight'] >= df['weight'].quantile(0.025)) & 
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculating the correlation matrix
    corr = df_heat.corr()

    #mask for upper traiangle
    mask=np.triu(np.ones_like(corr,dtype=bool))
    
    #matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    #plotting the correlation matrix
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", linewidths=.5,ax=ax)
    plt.savefig('heatmap.png')
    plt.show()
    plt.close(fig)


draw_heat_map()
    


