import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import *
from sklearn.decomposition import PCA  # pip install -U scikit-learn
import string
import nltk  # pip install nltk
# python        import nltk         nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  # nltk.download("punkt")
from nltk.stem import WordNetLemmatizer  # nltk.download("wordnet")
import math


courses = pd.read_csv("courses_edited.csv")
comments = pd.read_csv("comments_edited.csv")

color_text_sec = "#002D80"

color_bg = "#C4C3C2"
color_bg_sec = "#9DA4B3"

color_special = "#FF9100"

color_bg_alt = "#C4C3C2"
color_text_alt = "black"
color_text_alt_captions = "#333333"

color_sidebar ="#7E1F86"
color_sidebar_text = "white"

def style():
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.markdown(f"""
    <style>
        /*set background pattern*/
        [data-testid="stAppViewContainer"] {{
            background-color: #FFFFFF;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 1000'%3E%3Cg %3E%3Ccircle fill='%23FFFFFF' cx='50' cy='0' r='50'/%3E%3Cg fill='%23faf9fa' %3E%3Ccircle cx='0' cy='50' r='50'/%3E%3Ccircle cx='100' cy='50' r='50'/%3E%3C/g%3E%3Ccircle fill='%23f4f3f5' cx='50' cy='100' r='50'/%3E%3Cg fill='%23efecf0' %3E%3Ccircle cx='0' cy='150' r='50'/%3E%3Ccircle cx='100' cy='150' r='50'/%3E%3C/g%3E%3Ccircle fill='%23eae6eb' cx='50' cy='200' r='50'/%3E%3Cg fill='%23e4e0e6' %3E%3Ccircle cx='0' cy='250' r='50'/%3E%3Ccircle cx='100' cy='250' r='50'/%3E%3C/g%3E%3Ccircle fill='%23dfdae1' cx='50' cy='300' r='50'/%3E%3Cg fill='%23dad4dd' %3E%3Ccircle cx='0' cy='350' r='50'/%3E%3Ccircle cx='100' cy='350' r='50'/%3E%3C/g%3E%3Ccircle fill='%23d4ced8' cx='50' cy='400' r='50'/%3E%3Cg fill='%23cfc8d3' %3E%3Ccircle cx='0' cy='450' r='50'/%3E%3Ccircle cx='100' cy='450' r='50'/%3E%3C/g%3E%3Ccircle fill='%23cac2ce' cx='50' cy='500' r='50'/%3E%3Cg fill='%23c5bcc9' %3E%3Ccircle cx='0' cy='550' r='50'/%3E%3Ccircle cx='100' cy='550' r='50'/%3E%3C/g%3E%3Ccircle fill='%23c0b6c4' cx='50' cy='600' r='50'/%3E%3Cg fill='%23bab0c0' %3E%3Ccircle cx='0' cy='650' r='50'/%3E%3Ccircle cx='100' cy='650' r='50'/%3E%3C/g%3E%3Ccircle fill='%23b5aabb' cx='50' cy='700' r='50'/%3E%3Cg fill='%23b0a4b6' %3E%3Ccircle cx='0' cy='750' r='50'/%3E%3Ccircle cx='100' cy='750' r='50'/%3E%3C/g%3E%3Ccircle fill='%23ab9fb2' cx='50' cy='800' r='50'/%3E%3Cg fill='%23a699ad' %3E%3Ccircle cx='0' cy='850' r='50'/%3E%3Ccircle cx='100' cy='850' r='50'/%3E%3C/g%3E%3Ccircle fill='%23a193a8' cx='50' cy='900' r='50'/%3E%3Cg fill='%239c8ea4' %3E%3Ccircle cx='0' cy='950' r='50'/%3E%3Ccircle cx='100' cy='950' r='50'/%3E%3C/g%3E%3Ccircle fill='%2397889F' cx='50' cy='1000' r='50'/%3E%3C/g%3E%3C/svg%3E");
            background-attachment: fixed;
            background-size: contain;
        }}

        /*set the sidebar color*/
        section[data-testid="stSidebar"]>div:first-child{{
            top: -2px;
            background-color: {color_bg_alt};
        }}

        /*set sidebar text color*/
        section[data-testid="stSidebar"]>div:first-child a>span{{
            color: {color_text_alt} !important;
        }}

        /*add a rounded background to the plots*/
        div[data-testid="stArrowVegaLiteChart"] {{
            padding: 1em 1em 0 1em!important;
            border-radius: 10px;
            background-color: {color_bg};
        }}

        /*force the plots to be contained on their parent box*/
        canvas {{
            width: 100% !important;
            height:auto !important;
        }}

        /*Set the color for the "Me" of "UdeMe" title in the main page*/
        #welcome-on-udeme>div>span>span{{
            color: #a435f0 !important;
        }}

        /*set a rounded and blurred background to the page content for better readability*/
        section.main > div.block-container > div[style] > div {{
            border: 1em solid rgba(0, 0, 0, 0);
            border-radius: 10px;
            background-color: rgba(255, 255, 155, 0.07);
            backdrop-filter: blur(10px);
            box-sizing:content-box;
            left: -1em;
        }}

        /*hides streamlit hamburger menu button and header*/
        header[tabindex="-1"][data-testid="stHeader"] {{
            *display: none;
        }}

        /*set link colors to highlighted text color*/
        a {{
            color: {color_text_sec} !important;
        }}

        /*style the st.expander widget to look like a st.selector*/
        div[data-testid="stExpander"] {{
            background-color: {color_bg_sec};
            border-radius: 5px;
        }}

        /*style the widgets to make them look alike*/
        div.stNumberInput>div:first-of-type, div.stSelectbox>div{{
            border: 1px solid rgba(0,0,0,0.2);
            border-radius: 5px;
        }}

        /*encompass comments and courses into a coloured rounded rectangle*/
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:only-child {{
            background-color: {color_bg_alt};
            border: 0px none;
            border-radius: 10px;
            color: {color_text_alt};
            padding: 0.5em 0.5em 0.5em 0.5em;
        }}

        /*fix comment and course lists layout*/
        div[data-testid="stVerticalBlock"]:has(div[data-testid="stHorizontalBlock"]:only-child):not(section.main>div>div>div[data-testid="stVerticalBlock"]){{
            *box-sizing:content-box;
            width: 100%;
        }}
        
        /*fix comment and course lists layout*/
        div.element-container~div[style]:has(div[data-testid='stVerticalBlock']>div[data-testid='stHorizontalBlock']:only-child) {{
            *box-sizing:content-box;
            width: 100% !important;
        }}

        /*set the text color of the subheader in a listed course*/
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:only-child h3{{
            color:{color_text_alt};
        }}

        /*set the text color of the captions inside a listed course or comment*/
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"]:only-child div[data-testid="stCaptionContainer"]{{
            color: {color_text_alt_captions};
        }}

        /*round the borders of st.image*/
        div[data-testid="stImage"] > img {{
            border-radius: 8px;
        }}

        /*add an outline to the stars to make them more readable*/
        g svg path {{
            stroke: #000000;
            stroke-width: 1px;
            stroke-opacity: 0.5;
            stroke-linejoin: "round";
            paint-order: stroke;
        }}

        span.rating-container {{
            margin:0 0.5em 0 0.5em;
            padding:0.25em 0.5em 0.75em 0.5em;
        }}

        h1 a:not(.custom), h2 a:not(.custom), h3 a:not(.custom), h4 a:not(.custom), h5 a:not(.custom), h6 a:not(.custom) {{
            display:none;
        }}

        /*Style custom buttons to look like streamlit buttons*/
        button.custom-button {{
            background-color: {color_bg};
            border: 1px solid rgba(0,0,0,0.2);
            padding: 0.3em 0.6em 0.3em 0.6em;
            border-radius: 0.25rem;
        }}

        /*Style custom buttons to look like streamlit buttons*/
        button.custom-button:hover {{
            color: {color_text_sec};
            border: 1px solid {color_text_sec};
        }}

        /*Style custom buttons to look like streamlit buttons*/
        button.custom-button:focus {{
            background-color: {color_text_sec};
            box-shadow: 0 0 0 3px rgba(0, 45, 128, 0.25);
            border-radius: 0.25rem;
            background-clip: padding-box;
            background-size:initial;
            outline:0;
        }}

        /*Style custom buttons to look like streamlit buttons*/
        button.custom-button:focus p {{
            color: #ffffff !important;
        }}

    </style>
    """, True)

    return


def set_page(page, num):
    st.session_state[page + "_page_num"] = num
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
            # chiave univoca checkbox
            if st.checkbox(option, key=x+str(count), on_change=set_display_search_results, args=[False]):
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
    # response = requests.get("https://www.udemy.com" + url)
    # soup = BeautifulSoup(response.text, "html.parser")

    # image_tags = soup.find_all("img", attrs={"srcset": True})
    # if len(image_tags) > 0:
    # url = [img["srcset"] for img in image_tags][0].split(", ")[-1]

    # return url.split()[0]
    # else:
    if type == "course":
        return "https://s.udemycdn.com/meta/default-meta-image-v2.png"
    elif type == "author":
        return "https://play-lh.googleusercontent.com/dsCkmJE2Fa8IjyXERAcwc5YeQ8_NvbZ4_OI8LgqyjILpXUfS5YhEcnAMajKPrZI-og"


def get_courses():

    if (st.session_state["topic"][0] == "Any topic"):
        if (st.session_state["subcategory"][0] == "Any subcategory"):
            list = courses[courses['category'].isin(
                st.session_state["category"])]
        else:
            list = courses[courses['subcategory'].isin(
                st.session_state["subcategory"])]

    else:
        list = courses[courses['topic'].isin(st.session_state["topic"])]

    if (st.session_state["language"][0] != "Any language"):
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
    elif st.session_state.order == "Suggested ✨":
        list['avg_rating_round'] = list['avg_rating'].round(decimals=1)
        list.sort_values(['avg_rating_round', 'num_comments', 'num_subscribers'],
                         ascending=[False, False, False], inplace=True)

    return list


def draw_rating(rating):
    full_star = f"""<svg fill='{color_special}' xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="2 2 20 20">
    <path d="m7.85 19.1 1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95Z"/>
    </svg>"""
    half_star = f"""<svg fill='{color_special}' xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="2 2 20 20">
    <path d="M12 8.925v5.85l2.375 1.85-.9-3.025 2.25-1.6h-2.8ZM7.85 19.1l1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95Z"/>
    </svg>"""
    empty_star = f"""<svg fill='{color_special}' xmlns="http://www.w3.org/2000/svg" height="24" width="24" viewBox="2 2 20 20">
    <path d="M9.625 16.625 12 14.775l2.375 1.85-.9-3.025 2.25-1.6h-2.8L12 8.925 11.075 12h-2.8l2.25 1.6ZM7.85 19.1l1.55-5.125-4-2.9h5l1.6-5.3 1.6 5.3h5l-4 2.9 1.55 5.125L12 15.95ZM12 12.775Z"/>
    </svg>"""

    svg_html = "<span class='rating-container'><g>"

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
        + f"</g><span style='color:#000000;vertical-align:super;font-size:0.7em;opacity:0.75;'>("
        + str(rating)
        + "/5)</span></span>"
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


def getcoursetopcomm(id):  #
    course = getcourseinfo(id)
    course_comments = comments[comments['course_id'] == id]

    if (course_comments.size <= 5):
        return
    else:
        stop_words = set(stopwords.words("english"))
        stop_words = stop_words.union(set(stopwords.words("portuguese")))
        stop_words = stop_words.union(set(stopwords.words("spanish")))
        if course["language"].iloc[0] not in ["english", "portoguese", "spanish"]:
            stop_words = stop_words.union(
                set(stopwords.words(course["language"].iloc[0])))

        lemmatizer = WordNetLemmatizer()
        # st.write(stop_words)

        tf_matrix = {}
        doc_count_matrix = {}

        for index, comment in course_comments.iterrows():
            tokens = nltk.word_tokenize(comment["comment"])
            word_count = {}

            for t in tokens:
                if t.lower() not in stop_words and t.isalpha():
                    t = lemmatizer.lemmatize(t.lower())
                    if t in word_count:
                        word_count[t] += 1
                    else:
                        word_count[t] = 1

                    if t in doc_count_matrix:
                        doc_count_matrix[t] += 1
                    else:
                        doc_count_matrix[t] = 1

            tf_matrix[index] = {
                key: value / len(word_count) for key, value in word_count.items()}
            # st.write(word_count)
            # st.write(len(word_count))

        idf_matrix = {key: math.log(len(course_comments) / value)
                      for key, value in doc_count_matrix.items()}

        tf_idf_matrix = {}
        for key, comment in tf_matrix.items():
            tf_idf_matrix[key] = {word: tf * idf_matrix[word]
                                  for word, tf in comment.items()}

        # col1, col2, col3 =st.columns(3)
        # with col1:
        #    st.header("tf matrix")
        #    st.write(tf_matrix)

        # with col2:
        #    st.header("Idf matrix")
        #    st.write(idf_matrix)

        # with col3:
        #    st.header("Tf-Idf matrix")
        #    st.write(tf_idf_matrix)

        course_comments["score"] = None
        i = 0
        for key, comment in tf_idf_matrix.items():
            if len(comment) > 0:
                course_comments["score"].iloc[i] = sum(
                    comment.values())/len(comment)
            i = i + 1

        df_tf_idf = pd.DataFrame(tf_idf_matrix).T.fillna(0)
        # st.write(df_tf_idf)

        pca = PCA(n_components=3, random_state=16)

        df_pca = pd.DataFrame(
            data=pca.fit_transform(df_tf_idf),
            columns=[f"topic_{n}" for n in range(pca.n_components_)]
        )

        # st.write(df_pca)

        df_weights = pd.DataFrame(
            data=pca.components_,
            columns=idf_matrix.keys(),
            index=[f"topic_{n}" for n in range(pca.n_components_)]
        )

        df_weights = df_weights.T
        # st.write(df_weights)
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #    st.write(df_weights.sort_values("topic_0", ascending=False))
        # with col2:
        #    st.write(df_weights.sort_values("topic_1", ascending=False))
        # with col3:
        #    st.write(df_weights.sort_values("topic_2", ascending=False))
        keywords = []

        n_keys = 0
        for keyword in df_weights.sort_values("topic_0", ascending=False).index:
            if n_keys < 3:
                if keyword not in keywords:
                    keywords.append(keyword)
                    n_keys += 1
            else:
                break

        for keyword in df_weights.sort_values("topic_1", ascending=False).index:
            if n_keys < 5:
                if keyword not in keywords:
                    keywords.append(keyword)
                    n_keys += 1
            else:
                break

        for keyword in df_weights.sort_values("topic_2", ascending=False).index:
            if n_keys < 7:
                if keyword not in keywords:
                    keywords.append(keyword)
                    n_keys += 1
            else:
                break

        # st.header("Top comments")
        threshold = 1.3*course_comments["score"].mean()
        top_comments = course_comments[course_comments["score"] >= threshold].sort_values(
            "score", ascending=False)
        # st.write(top_comments)

    return top_comments[:10], keywords


def getauthorcourses(author):  #
    return courses[courses['instructor_url'] == author]


def coursesdb():  #
    return courses


def commentsdb():  #
    return comments


def counts():  #
    return len(courses), len(comments), len(courses["instructor_name"].unique())
