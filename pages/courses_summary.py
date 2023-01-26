import streamlit as st
import backend as be

be.style()

st.header("Courses summary")

st.write("")

courses=be.coursesdb()
comments=be.commentsdb()

courses, comments, instructors = be.counts()

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Total courses:")
    st.subheader(courses)

with col2:
    st.header("Total instructors:")
    st.subheader(instructors)

with col3:
    st.header("Total comments:")
    st.subheader(comments)
