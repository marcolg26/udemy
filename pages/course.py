import streamlit as st
import backend as be
import altair as alt
import pandas as pd


be.style()

arg = st.experimental_get_query_params()
# st.experimental_set_query_params()

if len(arg) == 0 or "cid" not in arg:
    st.header("Couldn't find this course, maybe it has been deleted")
else:
    course_ID = int(arg["cid"][0])

    course = be.getcourseinfo(course_ID)

    if course.size == 0:
        st.subheader("ID not found")
    else:
        col1, col2 = st.columns([2, 6])
        with col1:
            st.markdown("<style> img{vertical-align: middle;} </style>", True)
            st.image(be.find_udemy_img_url(course.course_url.iloc[0]))

        with col2:
            st.title(course['title'].iloc[0])
            st.write("<h3 style='padding-top:0;margin-top:0;'>Course by <a href='/author?u=" +
                     course.instructor_url.iloc[0] + "' target='_self' class='custom'>" + course.instructor_name.iloc[0] + "</a></h3>", unsafe_allow_html=True)

            if course.price.iloc[0] != 0:
                st.write(
                    "<h5>Price: " + str(course.price.iloc[0]) + "$</h5>", unsafe_allow_html=True)
            else:
                st.write("<h5 style'color:#117323;'>Free course!</h5>",
                         unsafe_allow_html=True)

            course_duration = course.content_length_min.iloc[0]
            if course_duration >= 120:
                st.write("<h6>" + str(round(course.num_lectures.iloc[0])) + " lectures (" + str(round(course_duration//60)) + " hours " + (str(round(
                    course_duration % 60)) if course_duration % 60 >= 10 else "0" + str(round(course_duration % 60))) + " minutes)</h6>", unsafe_allow_html=True)
            else:
                st.write("<h6>" + str(round(course.num_lectures.iloc[0])) + " lectures (" + str(
                    round(course_duration)) + " minutes)</h6>", unsafe_allow_html=True)
            st.write(
                f"""
                <a href='https://www.udemy.com{course.course_url.iloc[0]}'>
                    <button class="custom-button">
                        <div style='vertical-align:center;box-sizing:border-box'>
                            <p style='margin-bottom:0'>Visit on Udemy!</p>
                        </div>
                    </button>
                </a>""", unsafe_allow_html=True)

        st.write(
            "<hr size=2><h5 style='margin-top:1em;'>" + course.headline.iloc[0] + "</h5>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Published")
            st.write("<h5>" + str(pd.to_datetime(
                course['published_time'].iloc[0]).date()) + "</h5>", unsafe_allow_html=True)

        with col2:
            st.subheader("Last update")
            if course.last_update_date.iloc[0] is not None:
                st.write(
                    "<h5>" + course.last_update_date.iloc[0] + "</h5>", unsafe_allow_html=True)
            else:
                st.write("<h5 style='color:#444444'>-</h5>",
                         unsafe_allow_html=True)

        with col3:
            st.subheader("Average rating")

            rating_html = be.draw_rating(course.avg_rating.iloc[0])

            st.markdown(rating_html, True)

            st.write(
                "<h6>" + str(round(course.num_reviews.iloc[0])) + " total reviews </h6>", unsafe_allow_html=True)
            st.write(
                "<h6>" + str(round(course.num_comments.iloc[0])) + " total comments</h6>", unsafe_allow_html=True)

        with col4:
            st.subheader("Subscribers")
            st.write(
                "<h5>" + str(round(course.num_subscribers.iloc[0])) + " total reviews </h5>", unsafe_allow_html=True)

        st.header("Trend")
        comments = be.getcoursecomm(course_ID)

        chart = alt.Chart(comments[comments['course_id'] == course_ID]).mark_bar().encode(
            alt.X('yearmonth(date):T', title=None),
            alt.Y('count()', title="N° of comments")
        ).configure_mark(color=be.color_text_sec)

        st.altair_chart(chart, use_container_width=True)

        if (comments.size == 0):
            st.subheader("No comments :(")
        else:
            st.header("Comments")

            if "course_page_num" not in st.session_state:
                st.session_state.course_page_num = 1

            keywords_container = st.container()

            col1, col2 = st.columns(2)
            with col1:
                view_option = st.selectbox(
                    "View", ["Top comments", "All comments"])
            # top_comments_container = st.container()
            with col2:
                comments_order_container = st.container()

            top_comments, keywords = be.getcoursetopcomm(course_ID)

            if len(keywords) > 0:
                with keywords_container:
                    st.caption("Keywords")
                    css = f"""
                    <style>
                        span.custom-bubble {{
                            border:2px solid #666666;
                            border-radius:30px;
                            margin:0.1em 0.5em 0.1em 0.5em;
                            padding:0.25em 0.5em 0.25em 0.5em;
                            background-color: {be.color_bg_sec};
                            color: #666666;
                        }}

                        span.custom-bubble:hover {{
                            border:3px solid {be.color_text_sec};
                            margin:0 0.4em 0 0.4em;
                            padding:0.26em 0.6em 0.26em 0.6em;
                            color: {be.color_text_sec};
                        }}
                    </style>"""
                    keywords_html = css + "<div style='margin-bottom:1em'>"
                    for keyword in keywords:
                        keywords_html = keywords_html + "<span class='custom-bubble'>" + keyword + "</span>"
                    keywords_html = keywords_html + "</div>"
                    st.markdown(keywords_html, True)

            if view_option == "All comments":
                comment_num = len(comments)
                page_limit = 15

                if st.session_state.course_page_num*page_limit > comment_num:
                    comments = comments[(
                        st.session_state.course_page_num-1)*page_limit:]
                else:
                    comments = comments[(st.session_state.course_page_num-1)
                                        * page_limit:st.session_state.course_page_num*page_limit]

                st.subheader("All comments ("+str(comment_num)+")")

                with comments_order_container:
                    comments_order = st.selectbox("Order comments by", [
                                                  "Publishing date", "Rating (ascending)", "Rating (descending)"])

                if comments_order == "Rating (ascending)":
                    comments.sort_values(
                        by='rate', inplace=True, ascending=True)
                elif comments_order == "Rating (descending)":
                    comments.sort_values(
                        by='rate', inplace=True, ascending=False)
                elif comments_order == "Publishing date":
                    comments.sort_values(
                        by='date', inplace=True, ascending=False)

                for index, comment in comments.iterrows():
                    with st.container():
                        col1, col2 = st.columns([1000, 1])
                        with col1:
                            st.write("<div style='display:block;'><span style='font-size:1.1em;font-weight:bold;'>"+str(
                                comment['display_name'])+"</span><span style='padding:0 0 0.2em 2em;position:relative;bottom:0.2em;'>"+be.draw_rating(comment['rate']) + "</span></div>", unsafe_allow_html=True)
                            st.write(comment['comment'])
                        with col2:
                            st.empty()

            else:
                # with top_comments_container:
                comment_num = len(top_comments)
                page_limit = 15

                if st.session_state.course_page_num*page_limit > comment_num:
                    top_comments = top_comments[(
                        st.session_state.course_page_num-1)*page_limit:]
                else:
                    top_comments = top_comments[(
                        st.session_state.course_page_num-1)]

                if comment_num == 0:
                    st.write("No top comments")
                else:
                    st.subheader("Top comments ("+str(comment_num)+")")
                    for index, comment in top_comments.iterrows():
                        with st.container():
                            col1, col2 = st.columns([1000, 1])
                            with col1:
                                st.write("<div style='display:block;'><span style='font-size:1.1em;font-weight:bold;'>"+str(
                                    comment['display_name'])+"</span><span style='padding:0 0 0.2em 2em;position:relative;bottom:0.2em;'>"+be.draw_rating(comment['rate']) + "</span></div>", unsafe_allow_html=True)
                                st.write(comment['comment'])
                            with col2:
                                st.empty()

            with st.container():
                st.markdown("""
                    <style>
                        section.main>div.block-container>div[style]>div>div[style]:last-of-type>div {
                            width: 28em !important;
                            align: center !important;
                        }

                        section.main>div.block-container>div[style]>div>div[style]:last-of-type {
                            align-items: center !important;
                            justify-content: center !important;
                            position: relative !important;
                            left: 50vw !important;
                        }
                    </style>
                """, True)

                max_page_num = int(
                    1 + comment_num/page_limit) if comment_num % page_limit != 0 else int(comment_num/page_limit)

                col1, col2, col3, col4, col5, col6, col7 = st.columns(
                    7, gap="small")
                with col1:
                    if st.session_state.course_page_num > 1:
                        st.button("<", key="previous", on_click=be.set_page,
                                  args=["course", st.session_state.course_page_num-1])

                with col2:
                    if st.session_state.course_page_num > 1:
                        st.button("1", key="first",
                                  on_click=be.set_page, args=["course", 1])

                with col3:
                    if st.session_state.course_page_num > 2:
                        st.write("...")

                with col4:
                    st.button(str(st.session_state.course_page_num),
                              key="current", disabled=True)

                with col5:
                    if st.session_state.course_page_num < max_page_num - 1:
                        st.write("...")

                with col6:
                    if st.session_state.course_page_num < max_page_num:
                        st.button(str(max_page_num), key="last",
                                  on_click=be.set_page, args=["course", max_page_num])

                with col7:
                    if st.session_state.course_page_num < max_page_num:
                        st.button(">", key="next", on_click=be.set_page,
                                  args=["course", st.session_state.course_page_num+1])
