import streamlit as st
import backend as be
import pandas as pd
import altair as alt

be.style()

st.title("Courses summary")

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

    chart= alt.Chart(coursesdb[coursesdb['category']==category]).mark_bar().encode(y='subcategory', x='count()')
    chart.encoding.x.title = 'courses'

    st.altair_chart(chart, use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    st.subheader("Languages")

    source = pd.DataFrame(
    {"language": coursesdb["language"].unique(), "value": 0})

    for index, row in source.iterrows():
        source.loc[source['language'] == row["language"], ['value']]= len(coursesdb[coursesdb['language'] == row["language"]])
    
    pie= alt.Chart(source).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="language", type="nominal"),
    )

    st.altair_chart(pie, use_container_width=True)

with col2:
    st.subheader("Prices")

    price = pd.DataFrame({"price": ['Free', '<10', '<20', '<50', '<100', '100+'], "value": 0})
    
    price.loc[price['price'] == 'Free', ['value']]= len(coursesdb[coursesdb['price'] ==0])
    price.loc[price['price'] == '<10', ['value']]=  len(coursesdb[coursesdb['price'].between(1, 10)])
    price.loc[price['price'] == '<20', ['value']]=  len(coursesdb[coursesdb['price'].between(10, 20)])
    price.loc[price['price'] == '<50', ['value']]=  len(coursesdb[coursesdb['price'].between(20, 50)])
    price.loc[price['price'] == '<100', ['value']]= len(coursesdb[coursesdb['price'].between(50, 100)])
    price.loc[price['price'] == '100+', ['value']]= len(coursesdb[coursesdb['price'] >100])

    pie= alt.Chart(price).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(field="price", type="nominal"),
    )

    st.altair_chart(pie, use_container_width=True)


col1, col2 = st.columns(2)
with col1:
    st.subheader("New courses")

    chart=alt.Chart(coursesdb).mark_line().encode(
    x='year(published_time):T',
    y='count()')
    chart.encoding.x.title = 'month'
    chart.encoding.y.title = 'new courses'

    st.altair_chart(chart, use_container_width=True)


    




