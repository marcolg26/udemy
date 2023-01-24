import streamlit as st
import backend as be

be.style()

arg = st.experimental_get_query_params()

course_ID=int(arg["cid"][0])

course=be.getcourseinfo(course_ID)
comments=be.getcoursecomm(course_ID)

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