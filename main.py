import streamlit as st
import pandas as pd
import backend as be


be.style()
       
st.title("Welcome on Ude:violet[Me]!")

st.header("What are you looking for?")

queryNL = st.empty()
st.write("You don't know what you are looking for? Check the courses summary!")

be.create_selection_expander("language", be.languages())

col1, col2, col3 = st.columns(3)
with col1:
    be.create_selection_expander("category", be.categories())

with col2:
    be.create_selection_expander("subcategory", be.subcategories())

with col3:
    be.create_selection_expander("topic", be.topics())

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state["free"]=st.checkbox("Only free courses")
    
with col2:
    st.session_state["min"]=st.number_input("Minimum price", 0, disabled=st.session_state["free"])

with col3:
    st.session_state["max"]=st.number_input("Maximum price", min_value=1, value=int(be.maxprice()), disabled=st.session_state["free"])

col1, col2 = st.columns(2)
with col1:
    st.session_state.pub_date = st.selectbox("Publishing date", ["Last three months", "Last year", "Anytime"], index=2)
with col2:
    st.session_state.upd_date = st.selectbox("Last updated", ["Last three months", "Last year", "Anytime"], index=2)

col1, col2 = st.columns(2)
with col1:
    st.session_state.order = st.selectbox("Order results by", ["Rating", "Publishing date", "Subscriptions", "Engagement"])
with col2:
    order_period = st.empty()

#if "order" in st.session_state and st.session_state.order != "Subscriptions":
    #with order_period:
        #st.selectbox(st.session_state.order + " during", ["Today", "Last week", "Last month", "Last three months", "Last year", "Anytime"], index=5)
    
with queryNL:
    st.write("I'm looking for a course in " + be.list_to_string("language").lower() + " about " + be.list_to_string("category").lower())

if st.button("Search!"):

    courses = be.get_courses()

    if(courses.size==0): st.header("No results :(")
    else: st.header("Top results ("+str(len(courses))+")")

    for index, course in courses.iterrows():
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image(be.find_course_img_url(course.course_url))
            with col2:
                st.subheader(course.title)

                instructor_name = "<a href=\"/author?u=" + course.instructor_url + "\" target=\"_self\">" + course.instructor_name + "</a>"
                st.caption("Course by " + instructor_name, True)
    
                st.caption(str(round(course.num_subscribers)) + " people subscribed to this course")
                be.draw_rating(course.avg_rating)

                #comm = "<a href=\"/course?u=" + str(round(course.id)) + "\" target=\"_self\"> comments</a>"
    
                #st.caption("<span>" + str(round(course.num_reviews)) + " reviews and " + str(round(course.num_comments)) + comm + "</span>", True)
                
                st.caption("<span>" + str(round(course.num_reviews)) + " reviews and " + str(round(course.num_comments)) + " comments</span>", True)

                if course.price!=0:
                    st.caption("Price: **" + str(course.price) + "**$")
                else:
                    st.caption(":green[Free course!]")          
    
                if course.content_length_min >= 120:
                    st.caption("Duration: " + str(round(course.content_length_min//60)) + ":" + (str(round(course.content_length_min%60)) if course.content_length_min%60 >= 10 else "0" + str(round(course.content_length_min%60))) + " hours (" + str(round(course.num_lectures)) + " lectures)")
                else:
                    st.caption("Duration: " + str(round(course.content_length_min)) + " minutes (" + str(round(course.num_lectures)) + " lectures)")
                    
                st.write(course.headline)

                st.markdown("<a href=\"/course?cid=" + str(round(course.id)) + "\" target=\"_self\">View more</a>", True)
