import streamlit as st
import backend as be
import pandas as pd
import altair as alt

be.style()

st.header("Courses summary")

st.write("")

coursesdb=be.coursesdb()
commentsdb=be.commentsdb()

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

col1, col2 = st.columns(2)
with col1:
    st.subheader("Categories")

    alt.data_transformers.disable_max_rows()
    chart= alt.Chart(coursesdb).mark_bar().encode(y='category', x='count()')
    chart.encoding.x.title = 'courses'

    st.altair_chart(chart, use_container_width=True)

with col2:
    st.subheader("Subcategories")

    category = st.selectbox("Select category", options=be.categories(), index=0)

    coursesdb=coursesdb[coursesdb['category']==category]
    chart= alt.Chart(coursesdb).mark_bar().encode(y='subcategory', x='count()')
    chart.encoding.x.title = 'courses'

    st.altair_chart(chart, use_container_width=True)
