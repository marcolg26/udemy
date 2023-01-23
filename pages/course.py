import streamlit as st
import backend as be

st.session_state["course_id"]=7723

course=be.getcourseinfo(st.session_state["course_id"])
st.header(course['title'].iloc[0])

comments=be.getcoursecomm(st.session_state["course_id"])

if(comments.size==0): st.subheader("No comments :(")
else: st.subheader("Comments ("+str(len(comments))+")")

i=0
for comment in comments.iterrows():
    st.write(comments['display_name'].iloc[i]+":")
    be.draw_rating(comments['rate'].iloc[i])
    st.write(comments['comment'].iloc[i])
    i=i+1