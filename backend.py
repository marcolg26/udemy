import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup


courses = pd.read_csv("courses_edited.csv")
comments = pd.read_csv("comments_edited.csv")

def create_selection_expander(selectionType, options):
    st.session_state[selectionType] = ["Any " + selectionType]
    
    with st.expander("Select " + selectionType):
        selected = st.empty()
        for option in options:
            if st.checkbox(option):
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
    soup = BeautifulSoup(response.text, 'html.parser')
    
    image_tags = soup.find_all('img', attrs = {'srcset' : True})
    url = [img['srcset'] for img in image_tags][0].split(", ")[-1]
    
    return url.split()[0]
        

def get_courses():
    placeholder = pd.DataFrame(columns = ["id",
    "title",
    "is_paid",
    "price",
    "headline",
    "num_subscribers",
    "avg_rating",
    "num_reviews",
    "num_comments",
    "num_lectures",
    "content_length",
    "published_time",
    "last_update", 
    "category", 
    "subcategory", 
    "topic",
    "language",
    "course_url",
    "instructor_name",
    "instructor_url"])
    
    placeholder.loc['0'] = [4715, "Online Vegan Vegetarian Cooking School", True, 24.99, "Learn to cook delicious vegan recipes. Filmed over 15 years ago, watch the first 2hrs FREE to see if...", 2231, 3.75, 134, 42, 37, 1268, "2010-08-05T22:06:13Z", "2020-11-06", "Lifestyle", "Food & Beverage", "Vegan Cooking", "English", "/course/vegan-vegetarian-cooking-school/", "Angela Poch", "/user/angelapoch/"]
    
    placeholder.loc['1'] = [3, "Online testing school", False, 21.2, "Learn to test recipes.", 231, 3.5, 14, 412, 7, 68, "2010-08-05T22:06:13Z", "2020-11-06", "Technology", "Film & Beverage", "Test Cooking", "Italian", "/course/the-lean-startup-debunking-myths-of-entrepreneurship/", "Diavola Chick", "/user/ericries/"]

    return placeholder


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
    
    svg_html = svg_html + "</g><span style=\"color:gold;vertical-align:super;font-size:0.7em\">(" + str(rating) + "/5)</span>"
    st.caption(svg_html, True)
    return 


def switch_page(page_name):
    if page_name == "courses_summary":
        courses_summary.display()


def languages(): #
  return courses["language"].unique()

def categories(): #
  return courses["category"].unique()

def maxprice(): #
  return round(courses["price"].max(),0)


