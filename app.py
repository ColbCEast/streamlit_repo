# Here is some starter code to get the data:
import streamlit as st
from sklearn.datasets import fetch_openml
import pandas as pd
import plotly.express as px

titanic_sklearn = fetch_openml('titanic', version = 1, as_frame = True)

# Cache Data
@st.cache_data
def load_data():
    return titanic_sklearn.frame

df = load_data()

st.title("Titanic Exploration")


# Sidebar showing average age of subsets
with st.sidebar:
    subset_df = df[['survived','sex','age']]
    survived = st.radio('Survived?', options = ['Y', 'N'])
    gender = st.radio('Select Sex', options = ['M', 'F'])

    if survived == 'Y':
        survived_value = '1'
        output_survived = 'surviving'
    else:
        survived_value = '0'
        output_survived = 'deceased'

    if gender == 'M':
        sex = 'male'
        output_sex = 'males'
    else:
        sex = 'female'
        output_sex = 'females'

    df_summary = subset_df[(subset_df['survived'] == survived_value) & (subset_df['sex'] == sex)]

    avg_age = round(df_summary['age'].mean(), 2)

    st.write(f'The average age for {output_survived} {output_sex} was {avg_age}.')


# Graphics
left, right = st.columns(2)

choice = st.checkbox('Area Chart?')

with left:
    df_survived = df[df['survived'] == '1']
    pclass_survive = st.text_input('Which class was the passenger in?', value = '1', key = 'pclass_survive')
    df_class = df_survived[df_survived['pclass'] == int(pclass_survive)]
    
    if choice:
        fig = px.area(data_frame = df_class, y = 'fare', title = f'Fare for survivors in {pclass_survive} class')
    else:
        fig = px.histogram(data_frame = df_class, x = 'fare', title = f'Fare for survivors in {pclass_survive} class')
    st.plotly_chart(fig)

with right:
    df_deceased = df[df['survived'] == '0']
    pclass_decease = st.text_input('Which class was the passenger in?', value = '1', key = 'pclass_decease')
    df_class_decease = df_deceased[df_deceased['pclass'] == int(pclass_decease)]

    if choice:
        fig = px.area(data_frame = df_class_decease, y = 'fare', title = f'Fare for deceased passengers in {pclass_decease} class')
    else:
        fig = px.histogram(data_frame = df_class_decease, x = 'fare', title = f'Fare for deceased passengers in {pclass_decease} class')
    st.plotly_chart(fig)
