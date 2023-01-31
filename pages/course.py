import streamlit as st
import backend as be
import altair as alt
import pandas as pd
from sklearn.decomposition import PCA #pip install -U scikit-learn
import string
import nltk #pip install nltk
from nltk.corpus import stopwords #python        import nltk         nltk.download("stopwords")
from nltk.tokenize import word_tokenize #nltk.download("punkt")
from nltk.stem import WordNetLemmatizer #nltk.download("wordnet")
import math

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

            stop_words = set(stopwords.words(course.language))
            lemmatizer = WordNetLemmatizer()
            #st.write(stop_words)

            tf_matrix = {}
            doc_count_matrix = {}

            for index, comment in comments.iterrows():
                st.write(str(comment['display_name'])+":")
                st.caption(be.draw_rating(comment['rate']), True)
                st.write(comment['comment'])

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
                                
                tf_matrix[index] = {key: value / len(word_count) for key, value in word_count.items()}
                #st.write(word_count)
                #st.write(len(word_count))

            idf_matrix = {key: math.log(len(comments) / value) for key, value in doc_count_matrix.items()}

            tf_idf_matrix = {}
            for key, comment in tf_matrix.items():
                tf_idf_matrix[key] = {word: tf * idf_matrix[word] for word, tf in comment.items()}

            #col1, col2, col3 =st.columns(3)
            #with col1: 
            #    st.header("tf matrix")
            #    st.write(tf_matrix)

            #with col2:
            #    st.header("Idf matrix")
            #    st.write(idf_matrix)

            #with col3:
            #    st.header("Tf-Idf matrix")
            #    st.write(tf_idf_matrix)
            
            comments["score"] = None
            i=0
            for key, comment in tf_idf_matrix.items():
                if len(comment) > 0: 
                    comments["score"].iloc[i] = sum(comment.values())/len(comment)
                i = i + 1

            df_tf_idf = pd.DataFrame(tf_idf_matrix).T.fillna(0)
            #st.write(df_tf_idf)

            pca = PCA(n_components=3, random_state=16)

            df_pca = pd.DataFrame(
                data=pca.fit_transform(df_tf_idf),
                columns=[f"topic_{n}" for n in range(pca.n_components_)]
            )

            #st.write(df_pca)

            df_weights = pd.DataFrame(
                data=pca.components_,
                columns=idf_matrix.keys(),
                index=[f"topic_{n}" for n in range(pca.n_components_)]
            )

            df_weights = df_weights.T
            #st.write(df_weights)
            col1, col2, col3 = st.columns(3)
            with col1: 
                st.write(df_weights.sort_values("topic_0", ascending=False))
            with col2: 
                st.write(df_weights.sort_values("topic_1", ascending=False))
            with col3: 
                st.write(df_weights.sort_values("topic_2", ascending=False))

            st.header("Top comments")
            threshold = 1.3*comments["score"].mean()
            st.write(comments[comments["score"]>=threshold].sort_values("score", ascending=False))