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
    st.session_state["free"] = st.checkbox("Only free courses")

with col2:
    st.session_state["min"] = st.number_input(
        "Minimum price ($)", 0, disabled=st.session_state["free"])

with col3:
    st.session_state["max"] = st.number_input("Maximum price ($)", min_value=1, value=int(
        be.maxprice()), disabled=st.session_state["free"])

col1, col2 = st.columns(2)
with col1:
    st.session_state.pub_date = st.selectbox(
        "Publishing date", ["Last three months", "Last year", "Anytime"], index=2)

with col2:
    st.session_state.upd_date = st.selectbox(
        "Last updated", ["Last three months", "Last year", "Anytime"], index=2)

col1, col2 = st.columns(2)
with col1:
    st.session_state.order = st.selectbox(
        "Order results by", ["Suggested ✨", "PCRA", "Rating", "Subscriptions", "Publishing date"])

with col2:
    order_period = st.empty()

# if "order" in st.session_state and st.session_state.order != "Subscriptions":
    # with order_period:
    # st.selectbox(st.session_state.order + " during", ["Today", "Last week", "Last month", "Last three months", "Last year", "Anytime"], index=5)

with queryNL:
    st.write("I'm looking for a course in " + be.list_to_string("language").lower() +
             " about " + be.list_to_string("category").lower())

if "display_search_results" not in st.session_state:
    be.set_display_search_results(False)

if st.button("Search!"):
    be.set_display_search_results(True)

if st.session_state.display_search_results:
    courses = be.get_courses()

    if (courses.size == 0):
        st.header("No results :(")
    else:
        courses_num = len(courses)
        st.header("Top results ("+str(courses_num)+")")

        if "main_page_num" not in st.session_state:
            st.session_state.main_page_num = 1

        page_limit = 10
        if st.session_state.main_page_num*page_limit > courses_num:
            courses = courses[(st.session_state.main_page_num-1)*page_limit:]
        else:
            courses = courses[(st.session_state.main_page_num-1)
                              * page_limit:st.session_state.main_page_num*page_limit]

        for index, course in courses.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(be.find_udemy_img_url(course.course_url))
                with col2:
                    st.subheader(course.title)

                    instructor_name = "<a href=\"/author?u=" + course.instructor_url + \
                        "\" target=\"_self\">" + course.instructor_name + "</a>"
                    st.caption("Course by " + instructor_name, True)
                    st.caption("Published: " + str(pd.to_datetime(course['published_time']).date()) + ("" if course.last_update_date is None else ("; Last update: " + course.last_update_date)))

                    st.caption(str(round(course.num_subscribers)) +
                               " people subscribed to this course")
                    st.caption(be.draw_rating(course.avg_rating), True)

                    # comm = "<a href=\"/course?u=" + str(round(course.id)) + "\" target=\"_self\"> comments</a>"

                    # st.caption("<span>" + str(round(course.num_reviews)) + " reviews and " + str(round(course.num_comments)) + comm + "</span>", True)

                    st.caption("<span>" + str(round(course.num_reviews)) + " reviews and " +
                               str(round(course.num_comments)) + " comments</span>", True)

                    if course.price != 0:
                        st.caption("Price: **" + str(course.price) + "**$")
                    else:
                        st.caption(":green[Free course!]")

                    if course.content_length_min >= 120:
                        st.caption("Duration: " + str(round(course.content_length_min//60)) + ":" + (str(round(course.content_length_min % 60)) if course.content_length_min %
                                   60 >= 10 else "0" + str(round(course.content_length_min % 60))) + " hours (" + str(round(course.num_lectures)) + " lectures)")
                    else:
                        st.caption("Duration: " + str(round(course.content_length_min)) +
                                   " minutes (" + str(round(course.num_lectures)) + " lectures)")

                    st.write(course.headline)

                    #st.markdown("<a href=\"/course?cid=" + str(round(course.id)
                    #                                           ) + "\" target=\"_self\">View more</a>", True)
                    st.write(
                        f"""
                        <a href='/course?cid={str(round(course.id))}' target='_self'>
                            <button class="custom-button" style="margin-bottom:1em;">
                                <div style='vertical-align:center;box-sizing:content-box'>
                                    <p style='margin-bottom:0'>View more</p>
                                </div>
                            </button>
                        </a>""", unsafe_allow_html=True)

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
                1 + courses_num/page_limit) if courses_num % page_limit != 0 else int(courses_num/page_limit)

            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                7, gap="small")
            with col1:
                if st.session_state.main_page_num > 1:
                    st.button("<", key="previous", on_click=be.set_page,
                              args=["main", st.session_state.main_page_num-1])

            with col2:
                if st.session_state.main_page_num > 1:
                    st.button("1", key="first",
                              on_click=be.set_page, args=["main", 1])

            with col3:
                if st.session_state.main_page_num > 2:
                    st.write("...")

            with col4:
                st.button(str(st.session_state.main_page_num),
                          key="current", disabled=True)

            with col5:
                if st.session_state.main_page_num < max_page_num - 1:
                    st.write("...")

            with col6:
                if st.session_state.main_page_num < max_page_num:
                    st.button(str(max_page_num), key="last",
                              on_click=be.set_page, args=["main", max_page_num])

            with col7:
                if st.session_state.main_page_num < max_page_num:
                    st.button("\>", key="next", on_click=be.set_page,
                              args=["main", st.session_state.main_page_num+1])
