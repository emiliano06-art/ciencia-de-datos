import streamlit as st 
import pandas  as pd 

name_link ="https://:raw.githubusercontent.com/adsoftsito/ciencia-datos/refs"
names_data = pd.read_csv(names_link)

st.tittle=("streamlit and pods")
st.dataframe(names_data)