import streamlit as st
import backend as be

be.style()

instructor_url = st.experimental_get_query_params()
#st.experimental_set_query_params()

st.title("Instructor summary")

if len(instructor_url) == 0 or "u" not in instructor_url:
    st.header("Couldn't find this instructor, maybe his profile has been deleted")
else:
    courses = be.getauthorcourses(instructor_url["u"][0])

    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown("""
        <style>
            img:first-of-type {
                border-radius: 50% !important;
            }
        </style>
        """, True)
        st.image(be.find_udemy_img_url(instructor_url))

    with col2:
        st.header(courses['instructor_name'].iloc[0])

    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])    
    with col1:
        st.empty()
    
    with col2:
        st.subheader("Total courses:")
        st.write(str(len(courses)))
    
    with col3:
        st.subheader("Total students")
        st.write(str(int(courses["num_subscribers"].sum())))

        #for index, course in courses.iterrows():
            #st.write(str(int(course.num_subscribers)))

    with col4:
        st.subheader("Average rating")
        mean_rating = round(courses["avg_rating"].mean(), 2)
        st.write(be.draw_rating(mean_rating), unsafe_allow_html=True)
