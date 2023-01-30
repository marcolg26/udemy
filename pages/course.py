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
    comments = be.getcoursecomm(course_ID)

    if course.size == 0:
        st.subheader("ID not found")
    else:
        st.title(course['title'].iloc[0])

        st.header("Trend")


        chart=alt.Chart(comments[comments['course_id'] == course_ID]).mark_line().encode(
            x='year(date):T',
            y='count()')
        chart.encoding.x.title = 'month'
        chart.encoding.y.title = 'new comments'

        st.altair_chart(chart, use_container_width=True)

        st.subheader("Comments")

        st.session_state.commentsorder = st.selectbox(
        "Order comments by", ["Publishing date", "Rating (ascending)", "Rating (descending)"])
        
        if st.session_state.commentsorder == "Rating (ascending)":
            comments.sort_values(by='rate', inplace=True, ascending=True)        
        elif st.session_state.commentsorder == "Rating (descending)":
            comments.sort_values(by='rate', inplace=True, ascending=False)
        elif st.session_state.commentsorder == "Publishing date":
            comments.sort_values(by='date', inplace=True, ascending=False)

        if (comments.size == 0):
            st.subheader("No comments :(")
        else:
            st.subheader("Top comments ("+str(len(comments))+")")
            i = 0
            for comment in comments.iterrows():
                st.write(str(comments['display_name'].iloc[i])+":")
                st.caption(be.draw_rating(comments['rate'].iloc[i]), True)
                st.write(comments['comment'].iloc[i])
                i = i+1
