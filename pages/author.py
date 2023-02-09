import streamlit as st
import backend as be
import pandas as pd
import altair as alt


# style the page
be.style()

# get the instructor url from the URL parameter
instructor_url = st.experimental_get_query_params()

if len(instructor_url) == 0 or "u" not in instructor_url:
    st.title("Instructor summary")
    st.header("Couldn't find this instructor, maybe his profile has been deleted")
else:
    # show author image and information
    courses = be.get_author_courses(instructor_url["u"][0])

    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown(f"""
        <style>
            div.custom-image>img {{
                border-radius: 50% !important;
            }}
        </style>
        <div date-testid="stImage" class="custom-image">
            <img src="{be.find_udemy_img_url(instructor_url["u"][0], "author")}" alt="0" style="max-width: 100%;">
        </div>
        """, True)

    with col2:
        st.title(courses['instructor_name'].iloc[0])

    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        st.empty()

    with col2:
        st.header("Total courses:")
        st.subheader(str(len(courses)))

    with col3:
        st.header("Total students")
        st.subheader(str(int(courses["num_subscribers"].sum())))

    with col4:
        st.header("Average rating")
        mean_rating = round(courses["avg_rating"].mean(), 2)

        rating_html = be.draw_rating(mean_rating)

        st.markdown(rating_html, True)

        st.write("**" + str(round(courses.num_reviews.sum())) + "** total reviews and **" +
                 str(round(courses.num_comments.sum())) + "** total comments")

    # add a custom button to visit the author page on Udemy
    st.write(
        f"""
            <a href='https://www.udemy.com{instructor_url["u"][0]}'>
                <button class="custom-button">
                    <div style='vertical-align:center;box-sizing:border-box'>
                        <p style='margin-bottom:0'>Visit on Udemy!</p>
                    </div>
                </button>
            </a>""", unsafe_allow_html=True)

    # create some overview plots for the ratings
    st.header("Course ratings insight")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Rating per course")

        source = pd.DataFrame({
            "Average Rating": courses.avg_rating.values,
            "Course": courses.title.values
        })

        plot = alt.Chart(source).mark_bar().encode(
            alt.X("Average Rating", scale=alt.Scale(domain=(0, 5)), title=None),
            alt.Y("Course", title=None)
        ).configure_mark(color=be.color_special)

        st.altair_chart(plot, use_container_width=True)

        st.subheader("Number of courses by rating")

        plot = alt.Chart(source).mark_bar().encode(
            alt.X("Average Rating:Q", title=None,
                  bin=alt.Bin(extent=[0, 5], step=0.5)),
            alt.Y("count()", title=None)
        ).configure_mark(color=be.color_special)

        st.altair_chart(plot, use_container_width=True)

    with col2:
        st.subheader("Number of reviews and comments per course")

        sourceRev = pd.DataFrame({
            "N° interactions": courses.num_reviews.values,
            "Type": "Reviews",
            "Course": courses.title.values
        })

        sourceCom = pd.DataFrame({
            "N° interactions": courses.num_comments.values,
            "Type": "Comments",
            "Course": courses.title.values
        })

        source = pd.concat([sourceRev, sourceCom])

        plot = alt.Chart(source).mark_bar().encode(
            x=alt.X("N° interactions:Q", title=None),
            y=alt.Y("Type:N", title=None, axis=alt.Axis(labels=False)),
            color=alt.Color('Type', scale=alt.Scale(domain=["Comments", "Reviews"], range=[be.color_text_sec, be.color_special]), legend=alt.Legend(
                orient='top', direction='horizontal', title="Type of interaction:", titleAnchor='start')),
            row=alt.Row("Course:N", header=alt.Header(labelAlign="left", labelPadding=15,
                        labelColor="grey", labelAngle=0, labelLimit=100, labelFontSize=12), spacing=10, title = None),
            tooltip=["N° interactions:Q", "Type:N", "Course:N"]
        )

        st.altair_chart(plot, use_container_width=True)

    # create some plot to view the author activity
    st.header("Activity")

    placeholder = st.container()
    plot_select = st.selectbox(
        "View", options=["N° of subscribers", "Average rating"], index=0)

    if plot_select == "N° of subscribers":
        with placeholder:
            st.subheader(
                "Publish and update course dates with number of subscribers")
    else:
        with placeholder:
            st.subheader("Publish and update course dates with rating")

    sourcePub = pd.DataFrame({
        "Date": pd.to_datetime(courses['published_time']).dt.date,
        "N° of subscribers": courses["num_subscribers"],
        "Average rating": courses["avg_rating"],
        "Type": "Pubblication",
        "Course": courses.title.values
    })

    sourceUp = pd.DataFrame({
        "Date": pd.to_datetime(courses['last_update_date']).dt.date,
        "N° of subscribers": courses["num_subscribers"],
        "Average rating": courses["avg_rating"],
        "Type": "Last update",
        "Course": courses.title.values
    })

    source = pd.concat([sourcePub, sourceUp]).sort_values(plot_select)

    plot = alt.Chart(source)

    line = plot.mark_line(opacity=0.5, strokeWidth=2, color="white").encode(
        alt.X("yearmonth(Date):T", title=None),
        y=plot_select
    )

    points = plot.mark_point(size=80, filled=True, point="transparent", opacity=1).encode(
        alt.X("yearmonth(Date):T"),
        alt.Y(plot_select, axis=alt.Axis(titleAnchor="start",
              titleAngle=0, titleY=-15, titleAlign="center")),
        color=alt.Color('Type', scale=alt.Scale(
            domain=["Last update", "Pubblication"], range=[be.color_special, be.color_text_sec])),
        shape=alt.Shape("Type:N", scale=alt.Scale(
            domain=["Last update", "Pubblication"], range=["cross", "circle"])),
        tooltip=[plot_select, "Date:T", "Course:N"]
    )

    st.altair_chart(line + points, use_container_width=True)

    # show the courses teached by the author
    st.header("Courses from this instructor")

    if (courses.size == 0):
        st.header("No results :(")
    else:
        courses_num = len(courses)

        # set up sub-page system
        if "author_page_num" not in st.session_state:
            st.session_state.author_page_num = 1

        page_limit = 10
        if st.session_state.author_page_num*page_limit > courses_num:
            courses = courses[(st.session_state.author_page_num-1)*page_limit:]
        else:
            courses = courses[(st.session_state.author_page_num-1)
                              * page_limit:st.session_state.author_page_num*page_limit]

        for index, course in courses.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(be.find_udemy_img_url(course.course_url))

                # display the course information
                with col2:
                    st.subheader(course.title)

                    # add a link on the course author name to the author page
                    instructor_name = "<a href=\"/author?u=" + course.instructor_url + \
                        "\" target=\"_self\">" + course.instructor_name + "</a>"
                    st.caption("Course by " + instructor_name, True)

                    st.caption("Published: " + str(pd.to_datetime(course['published_time']).date()) + (
                        "" if course.last_update_date is None else ("; Last update: " + course.last_update_date)))

                    st.caption(str(round(course.num_subscribers)) +
                               " people subscribed to this course")

                    st.caption(be.draw_rating(course.avg_rating), True)

                    st.caption("<span>" + str(round(course.num_reviews)) + " reviews and " +
                               str(round(course.num_comments)) + " comments</span>", True)

                    if course.price != 0:
                        st.caption("Price: **" + str(course.price) + "**$")
                    else:
                        st.caption(":green[Free course!]")

                    # represent the duration in minutes if the duration is less than 2 hours, otherwise it is converted in hours and minutes
                    if course.content_length_min >= 120:
                        st.caption("Duration: " + str(round(course.content_length_min//60)) + ":" + (str(round(course.content_length_min % 60)) if course.content_length_min %
                                   60 >= 10 else "0" + str(round(course.content_length_min % 60))) + " hours (" + str(round(course.num_lectures)) + " lectures)")
                    else:
                        st.caption("Duration: " + str(round(course.content_length_min)) +
                                   " minutes (" + str(round(course.num_lectures)) + " lectures)")

                    st.write(course.headline)

                    # add a custom button to go to the course page
                    st.write(
                        f"""
                        <a href='/course?cid={str(round(course.id))}' target='_self'>
                            <button class="custom-button" style="margin-bottom:1em;">
                                <div style='vertical-align:center;box-sizing:content-box'>
                                    <p style='margin-bottom:0'>View more</p>
                                </div>
                            </button>
                        </a>""", unsafe_allow_html=True)

        # adds buttons for the sub-page system and styles them
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
                if st.session_state.author_page_num > 1:
                    st.button("<", key="previous", on_click=be.set_page,
                              args=["author", st.session_state.author_page_num-1])

            with col2:
                if st.session_state.author_page_num > 1:
                    st.button("1", key="first",
                              on_click=be.set_page, args=["author", 1])

            with col3:
                if st.session_state.author_page_num > 2:
                    st.write("...")

            with col4:
                st.button(str(st.session_state.author_page_num),
                          key="current", disabled=True)

            with col5:
                if st.session_state.author_page_num < max_page_num - 1:
                    st.write("...")

            with col6:
                if st.session_state.author_page_num < max_page_num:
                    st.button(str(max_page_num), key="last",
                              on_click=be.set_page, args=["author", max_page_num])

            with col7:
                if st.session_state.author_page_num < max_page_num:
                    st.button("\>", key="next", on_click=be.set_page,
                              args=["author", st.session_state.author_page_num+1])
