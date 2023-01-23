import streamlit as st


st.set_page_config(layout="wide")

instructor_url = st.experimental_get_query_params()

st.title("Instructor summary")

if len(instructor_url) == 0:
    st.header("Couldn't find this instructor, maybe his profile has been deleted")
else:
    st.header(instructor_url["u"][0])