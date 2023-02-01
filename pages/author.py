import streamlit as st
import backend as be
import pandas as pd
import altair as alt


be.style()

instructor_url = st.experimental_get_query_params()
# st.experimental_set_query_params()

if len(instructor_url) == 0 or "u" not in instructor_url:
    st.title("Instructor summary")
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
        st.image(be.find_udemy_img_url(instructor_url, "author"))

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

        rating_html = be.draw_rating(mean_rating).split("<g>")
        rating_html = rating_html[0] + \
            "<g transform='scale(0.1, 10)'>" + rating_html[1]

        # st.markdown("""
        # <style>
        #    g {
        #        display:block;
        #   }
        # </style>
        # """, True)

        st.markdown(rating_html, True)

        st.write("**" + str(round(courses.num_reviews.sum())) + "** total reviews and **" +
                 str(round(courses.num_comments.sum())) + "** total comments")

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
                        labelColor="white", labelAngle=0, labelLimit=100, labelFontSize=12), spacing=10),
            tooltip=["N° interactions:Q", "Type:N", "Course:N"]
        )

        st.altair_chart(plot, use_container_width=True)

    st.header("Activity")

    placeholder = st.container()
    plot_select = st.selectbox("View", options=["N° of subscribers", "Average rating"], index=0)

    if plot_select == "N° of subscribers":
        with placeholder: st.subheader("Publish and update course dates with number of subscribers")
    else:
        with placeholder: st.subheader("Publish and update course dates with rating")

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