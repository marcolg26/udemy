import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import *


courses = pd.read_csv("courses_edited.csv")
comments = pd.read_csv("comments_edited.csv")


def style():
    st.set_page_config(layout="wide")

    st.markdown("""
    <style>
        button[title="View fullscreen"]{
            visibility: hidden;
        }
            
        a {
            color: #b27eff !important;
        }

        div[data-testid="stExpander"], 
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:only-child{
            /*background-color: #262626;*/
            background-color: #262730;
            /*border: 1px solid #5f5760;*/
            border: 0px none #262730;
            border-radius: 5px;
        }
        
        div[data-testid="stImage"] > img{
            align-items: center;
            border-radius: 5px;
        }
    </style>
    """, True)

    return


def set_page(num):
    st.session_state.page_num = num 
    return

def set_display_search_results(b):
    st.session_state.display_search_results = b

def create_selection_expander(selectionType, options):
    count = 0
    st.session_state[selectionType] = ["Any " + selectionType]

    x = "d"
    if selectionType == "category":
        x = "a"
    elif selectionType == "subcategory":
        x = "b"
    elif selectionType == "topic":
        x = "c"
    elif selectionType == "language":
        x = "e"

    with st.expander("Select " + selectionType):
        selected = st.empty()
        for option in options:
            count = count+1
            if isinstance(option, float):
                option = "(other)"  # per evitare valori nan
            if st.checkbox(option, key=x+str(count), on_change=set_display_search_results, args=[False]):  # chiave univoca checkbox
                st.session_state[selectionType].append(option)
                if "Any " + selectionType in st.session_state[selectionType]:
                    st.session_state[selectionType].remove(
                        "Any " + selectionType)

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


def find_udemy_img_url(url, type="course"):
    #response = requests.get("https://www.udemy.com" + url)
    #soup = BeautifulSoup(response.text, "html.parser")

    #image_tags = soup.find_all("img", attrs={"srcset": True})
    #if len(image_tags) > 0:
        #url = [img["srcset"] for img in image_tags][0].split(", ")[-1]

        #return url.split()[0]
    #else:
        if type == "course":
            return "https://s.udemycdn.com/meta/default-meta-image-v2.png"
        elif type == "author":
            return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og"


def get_courses():

    if(st.session_state["topic"][0]=="Any topic"):
        if(st.session_state["subcategory"][0]=="Any subcategory"):
            list = courses[courses['category'].isin(st.session_state["category"])]
        else:
            list = courses[courses['subcategory'].isin(st.session_state["subcategory"])]

    else: list = courses[courses['topic'].isin(st.session_state["topic"])]

    list = list[list['language'].isin(st.session_state["language"])]
    if st.session_state["free"]:
        list = list[list['price'] == 0]
    else:
        list = list[list['price'] <= st.session_state["max"]]
    list = list[list['price'] >= st.session_state["min"]]

    if st.session_state.pub_date != "Anytime":

        use_date = datetime.datetime.now()

        if st.session_state.pub_date == "Last year":
            use_date = use_date + datetime.timedelta(days=-365)
        elif st.session_state.pub_date == "Last tree months":
            use_date = use_date + datetime.timedelta(days=-90)

        use_date1 = use_date.date()

        list['published_time'] = pd.to_datetime(list['published_time']).dt.date

        list = list[list['published_time'] > use_date1]

    if st.session_state.upd_date != "Anytime":

        use_date = datetime.datetime.now()

        if st.session_state.upd_date == "Last year":
            use_date = use_date + datetime.timedelta(days=-365)
        elif st.session_state.upd_date == "Last tree months":
            use_date = use_date + datetime.timedelta(days=-90)

        use_date1 = use_date.date()

        list['last_update_date'] = pd.to_datetime(
            list['last_update_date']).dt.date

        list = list[list['last_update_date'] > use_date1]

    if st.session_state.order == "Subscriptions":
        list.sort_values(by='num_subscribers', inplace=True, ascending=False)
    elif st.session_state.order == "Rating":
        list.sort_values(by='avg_rating', inplace=True, ascending=False)
    elif st.session_state.order == "Publishing date":
        list.sort_values(by='published_time', inplace=True, ascending=False)

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
    
    return svg_html


def languages():  #
    return courses["language"].unique()


def categories():  #
    return courses["category"].unique()


def subcategories():  #
    sub = courses[courses['category'].isin(st.session_state["category"])]
    return sub["subcategory"].unique()


def topics():  #
    top = courses[courses['subcategory'].isin(st.session_state["subcategory"])]
    return top["topic"].unique()


def maxprice():  #
    return round(courses["price"].max(), 0)


def getcourseinfo(id):  #
    return courses[courses['id'] == id]


def getcoursecomm(id):  #
    return comments[comments['course_id'] == id]


def getauthorcourses(author):  #
    return courses[courses['instructor_url'] == author]

def stats():  #
    return courses['category'].value_counts()
