import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import BaggingClassifier

st.title('Prediction of COVID-19')
with st.expander('Data'):
  data = pd.read_csv("covid-19 symptoms dataset.csv")
