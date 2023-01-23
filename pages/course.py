import streamlit as st
import backend as be

<<<<<<< HEAD
st.set_page_config(layout="wide")

course_id = st.experimental_get_query_params()

if len(course_id) == 0:
    st.header("Couldn't find this course, maybe it has been deleted")
else:
    course_id = float(course_id["cid"][0])

course=be.getcourseinfo(course_id)
st.header(course['title'].iloc[0])

comments=be.getcoursecomm(course_id)
=======
arg = st.experimental_get_query_params()

course_ID=int(arg["u"][0])

course=be.getcourseinfo(course_ID)
comments=be.getcoursecomm(course_ID)
>>>>>>> e5bab6d14d373fefd28ccbc52486dc3193dd6e12

if(course.size==0): st.subheader("ID not found")
else:
    st.header(course['title'].iloc[0])
    
    if(comments.size==0): st.subheader("No comments :(")
    else:
        st.subheader("Comments ("+str(len(comments))+")")
        i=0
        for comment in comments.iterrows():
            st.write(str(comments['display_name'].iloc[i])+":")
            be.draw_rating(comments['rate'].iloc[i])
            st.write(comments['comment'].iloc[i])
            i=i+1