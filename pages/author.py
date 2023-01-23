import streamlit as st
import backend as be

st.set_page_config(layout="wide")

instructor_url = st.experimental_get_query_params()

st.title("Instructor summary")

if len(instructor_url) == 0:
    st.header("Couldn't find this instructor, maybe his profile has been deleted")
else:
    st.header(instructor_url["u"][0])

    courses=be.getauthorcourses(instructor_url["u"][0])

    i=0
    for course in courses.iterrows():
        st.write(courses['title'].iloc[i])
        i=i+1