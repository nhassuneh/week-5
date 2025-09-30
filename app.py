import streamlit as st
from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
'''
# Titanic Visualization 1

'''
)

# Question for Exercise 1
st.write("Question: Which age range has the highest average survival rate?")

# Display the plot
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write("Based on the data, the age range with the highest average survival rate is Child.")
'''
# Titanic Visualization 2
'''
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)