import streamlit as st
import pandas as pd
from pathlib import Path
import os
import time

path1 = Path('courses_edited.csv')
path2 = Path('comments_edited.csv')
st.header("Test csv -> loading file saved in streamlit cloud")

st.subheader("Courses")
if path1.is_file(): 
    courses = pd.read_csv('courses_edited.csv')
    st.write("Courses file already exists ✓")
    ti_c = os.path.getctime(path1)
    c_ti = time.ctime(ti_c)
    st.write("Last modified: "+c_ti)
    st.write("Size: "+str(len(courses)))

else:
    st.write("Courses file doesn't exists ✗")
    if st.button("Download"):
        url="https://marcolg.altervista.org/drive/courses_edited.csv"
        courses=pd.read_csv(url)
        courses.to_csv('courses_edited.csv')
        st.write("File created now ✓")

st.subheader("Comments")
if path2.is_file(): 
    comments = pd.read_csv('comments_edited.csv')
    st.write("Comments file already exists ✓")
    ti_c = os.path.getctime(path2)
    c_ti = time.ctime(ti_c)
    st.write("Last modified: "+c_ti)
    st.write("Size: "+str(len(comments)))

else:
    st.write("Comments file doesn't exists ✗")
    if st.button("Download"):
        url="https://marcolg.altervista.org/drive/comments_edited.csv"
        comments=pd.read_csv(url)
        comments.to_csv('comments_edited.csv')
        st.write("File created now ✓")
