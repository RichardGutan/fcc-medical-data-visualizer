import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv', delimiter=',')

# Add 'overweight' column
bmi = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (bmi > 25).astype('int8')

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc'] = (df['gluc'] > 1).astype('int8')
df['cholesterol'] = (df['cholesterol'] > 1).astype('int8')




# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat3 = (
        df_cat
        .groupby(['cardio', 'variable'])['value']
        .value_counts()
        .rename('total')
        .reset_index()
    )

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(kind="bar", x="variable", y="total", hue="value", col="cardio", data=df_cat3)

    # Do not modify the next two lines
    g.savefig('catplot.png')
    return g.fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[df['ap_lo'] <= df['ap_hi']]
    df_heat = df_heat[df_heat['height'] >= df_heat['height'].quantile(0.025)]
    df_heat = df_heat[df_heat['height'] <= df_heat['height'].quantile(0.975)]
    df_heat = df_heat[df_heat['weight'] >= df_heat['weight'].quantile(0.025)]
    df_heat = df_heat[df_heat['weight'] <= df_heat['weight'].quantile(0.975)]
    

    # Calculate the correlation matrix
    corr = df_heat.corr()
   
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True


    # Set up the matplotlib figure
    fig = plt.figure()
    ax = plt.axes()
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, mask=mask, ax=ax, annot=True, fmt='.1f')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
