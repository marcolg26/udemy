import streamlit as st
import backend as be
import altair as alt


be.style()

arg = st.experimental_get_query_params()
#st.experimental_set_query_params()

if len(arg) == 0 or "cid" not in arg:
    st.header("Couldn't find this course, maybe it has been deleted")
else:
    course_ID = int(arg["cid"][0])

    course = be.getcourseinfo(course_ID)

    if course.size == 0:
        st.subheader("ID not found")
    else:
        col1, col2 = st.columns([1, 6])
        with col1:
            st.markdown("<style> img{vertical-align: middle;} </style>", True)
            st.image(be.find_udemy_img_url(course.course_url))
        
        with col2:
            st.title(course['title'].iloc[0])
            st.subheader("Course by " + course.instructor_name.iloc[0])

        st.header("Trend")
        comments = be.getcoursecomm(course_ID)

        chart=alt.Chart(comments[comments['course_id'] == course_ID]).mark_line().encode(
            x='year(date):T',
            y='count()')
        chart.encoding.x.title = 'month'
        chart.encoding.y.title = 'new comments'

        st.altair_chart(chart, use_container_width=True)

        if (comments.size == 0):
            st.subheader("No comments :(")
        else:
            st.header("Comments")
            col1, col2, col3 = st.columns(3)
            with col1:
                view_option = st.selectbox("View", ["Top comments", "All comments"])
            top_comments_container = st.container()
            with col2:
                comments_order_container = st.container()

            if view_option == "All comments":
                st.subheader("All comments ("+str(len(comments))+")")
                with comments_order_container:
                    comments_order = st.selectbox("Order comments by", ["Publishing date", "Rating (ascending)", "Rating (descending)"])
                
                if comments_order == "Rating (ascending)":
                    comments.sort_values(by='rate', inplace=True, ascending=True)        
                elif comments_order == "Rating (descending)":
                    comments.sort_values(by='rate', inplace=True, ascending=False)
                elif comments_order == "Publishing date":
                    comments.sort_values(by='date', inplace=True, ascending=False)

                for index, comment in comments.iterrows():
                    with st.container():
                        col1, col2 = st.columns([1000, 1])
                        with col1:
                            st.write("<div style='display:block;'><span style='font-size:1.1em;font-weight:bold;'>"+str(comment['display_name'])+"</span><span style='padding:0 0 0.2em 2em;position:relative;bottom:0.2em;'>"+be.draw_rating(comment['rate'])+ "</span></div>", unsafe_allow_html=True)
                            st.write(comment['comment'])
                        with col2:
                            st.empty()

            else:
                with top_comments_container:
                    top_comments = be.getcoursetopcomm(course_ID)
                    if len(top_comments) == 0:
                        st.write("No top comments")
                    else:
                        st.subheader("Top comments ("+str(len(top_comments))+")")
                        for index, comment in top_comments.iterrows():
                            with st.container():
                                col1, col2 = st.columns([1000, 1])
                                with col1:
                                    st.write("<div style='display:block;'><span style='font-size:1.1em;font-weight:bold;'>"+str(comment['display_name'])+"</span><span style='padding:0 0 0.2em 2em;position:relative;bottom:0.2em;'>"+be.draw_rating(comment['rate'])+ "</span></div>", unsafe_allow_html=True)
                                    st.write(comment['comment'])
                                with col2:
                                    st.empty()