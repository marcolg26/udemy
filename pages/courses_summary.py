import streamlit as st
import backend as be

be.style()

st.header("Courses summary")

st.write("Brief insight on what should you want to learn given what we can discover using the exploration of our dataset")

categories=be.stats()

print(categories.info())

categories.plot()