import pandas as pd
import requests
import streamlit as st
import math
from bs4 import BeautifulSoup


courses = pd.read_csv("courses_edited.csv")
comments = pd.read_csv("comments_edited.csv")


def create_selection_expander(selectionType, options):
    count=0 
    st.session_state[selectionType] = ["Any " + selectionType]

    x="d"
    if selectionType=="category": x="a"
    elif selectionType=="subcategory": x="b"
    elif selectionType=="topic": x="c"
    elif selectionType=="language": x="e"
   
    with st.expander("Select " + selectionType):
        selected = st.empty()
        for option in options:
            count=count+1
            if isinstance(option, float): option="(other)" #per evitare valori nan
            if st.checkbox(option, key=x+str(count)): #chiave univoca checkbox
                st.session_state[selectionType].append(option)
                if "Any " + selectionType in st.session_state[selectionType]:
                    st.session_state[selectionType].remove("Any " + selectionType)

            elif option in st.session_state[selectionType]:
                st.session_state[selectionType].remove(option)

    with selected:
        st.caption("Selection: " + list_to_string(selectionType).lower())


def list_to_string(selector):
    string = ""
    if selector in st.session_state:
        string = string + st.session_state[selector][0]
        n = len(st.session_state[selector])
        if n > 1:
            for element in st.session_state[selector][1:]:
                string = string + ", " + element

    return string


def find_course_img_url(course_url):
    response = requests.get("https://www.udemy.com" + course_url)
    soup = BeautifulSoup(response.text, "html.parser")

    image_tags = soup.find_all("img", attrs={"srcset": True})
    url = [img["srcset"] for img in image_tags][0].split(", ")[-1]

    return url.split()[0]


def get_courses():

    list = courses[courses['topic'].isin(st.session_state["topic"])]
    list=list[list['language'].isin(st.session_state["language"])]
    if st.session_state["free"]:
        list = list[list['price']==0]
    else: list = list[list['price']<=st.session_state["max"]]
    list = list[list['price']>=st.session_state["min"]]

    return list


def draw_rating(rating):
    full_star = """<svg fill='gold' xmlns="http://www.w3.org/2000/svg" height="24" width="24">
    <path d="m7.85 19.1 1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95Z"/>
    </svg>"""
    half_star = """<svg fill='gold' xmlns="http://www.w3.org/2000/svg" height="24" width="24">
    <path d="M12 8.925v5.85l2.375 1.85-.9-3.025 2.25-1.6h-2.8ZM7.85 19.1l1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95Z"/>
    </svg>"""
    empty_star = """<svg fill='gold' xmlns="http://www.w3.org/2000/svg" height="24" width="24">
    <path d="M9.625 16.625 12 14.775l2.375 1.85-.9-3.025 2.25-1.6h-2.8L12 8.925 11.075 12h-2.8l2.25 1.6ZM7.85 19.1l1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95ZM12 12.775Z"/>
    </svg>"""

    svg_html = "<g>"

    for i in range(1, 6):
        diff = rating - i
        if diff >= -0.25:
            svg_html = svg_html + full_star
        elif diff + 0.5 >= -0.25:
            svg_html = svg_html + half_star
        else:
            svg_html = svg_html + empty_star

    svg_html = (
        svg_html
        + '</g><span style="color:gold;vertical-align:super;font-size:0.7em">('
        + str(rating)
        + "/5)</span>"
    )
    st.caption(svg_html, True)
    return


def languages():  #
    return courses["language"].unique()


def categories():  #
    return courses["category"].unique()


def subcategories():  #
    sub=courses[courses['category'].isin(st.session_state["category"])]
    return sub["subcategory"].unique()

def topics():  #
    top=courses[courses['subcategory'].isin(st.session_state["subcategory"])]
    return top["topic"].unique()


def maxprice():  #
    return round(courses["price"].max(), 0)
