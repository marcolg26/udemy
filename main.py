import streamlit as st
import pandas as pd
import backend as be 

#prova

st.set_page_config(layout="wide")

st.markdown("""
<style>
    button[title="View fullscreen"]{
        visibility: hidden;
    }
        
    div[data-testid="stExpander"], 
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:only-child{
        background-color: #262626;
        border: 1px solid #5f5760;
        border-radius: 5px;
    }
    
    div[data-testid="stImage"] > img{
        align-items: center;
        border-radius: 5px;
    }
</style>
""", True)
    
    
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
    st.checkbox("Only free courses")

with col2:
    st.number_input("Minimum price", 0)

with col3:
    st.number_input("Maximum price", be.maxprice())
    
with queryNL:
    st.write("I'm looking for a course in " + be.list_to_string("language").lower() + " about " + be.list_to_string("category").lower())

if st.button("Search!"):

    courses = be.get_courses()
    
    st.header("Top results")
    
    for index, course in courses.iterrows():
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image(be.find_course_img_url(course.course_url))
            with col2:
                
                st.subheader(course.title)

                instructor_name = "<a href=\"/author\" target=\"self\">" + course.instructor_name + "</a>"
                st.caption("Course by " + instructor_name, True)
    
                st.caption(str(course.num_subscribers) + " people subscribed to this course")
                be.draw_rating(course.avg_rating)
    
                st.caption("<span>" + str(course.num_reviews) + " reviews and " + str(course.num_comments) + " comments: " + "</span>", True)
                
                if course.price==0:
                    st.caption("Price: **" + str(course.price) + "** $")
                else:
                    st.caption(":green[Free course!]")          
    
                if course.content_length_min >= 120:
                    st.caption("Duration: " + str(course.content_length_min//60) + ":" + (str(course.content_length_min%60) if course.content_length_min%60 >= 10 else "0" + str(course.content_length_min%60)) + " hours (" + str(course.num_lectures) + " lectures)")
                else:
                    st.caption("Duration: " + str(course.content_length_min) + " minutes (" + str(course.num_lectures) + " lectures)")
                    
                st.write(course.headline)
