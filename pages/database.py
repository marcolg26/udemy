import streamlit as st
import pandas as pd
from pathlib import Path
import os
import time


path1 = Path('courses_edited.csv')
path2 = Path('comments_edited.csv')

st.header("Databases status")

st.subheader("Courses")
if path1.is_file():

    courses = pd.read_csv(path1)
    st.write("Courses file already exists ✓")
    st.write("Last modified: "+time.ctime(os.path.getctime(path1)))
    st.write("Size: "+str(len(courses))+" records")

    if st.button("Update", key="courUP"):
        os.remove(path1)
        url="https://marcolg.altervista.org/drive/courses_edited.csv"
        courses=pd.read_csv(url)
        courses.to_csv(path1)
        st.write("File updated ✓")
        st.experimental_rerun()

else:
    st.write("Courses file doesn't exists ✗")
    if st.button("Download", key="cour"):
        url="https://marcolg.altervista.org/drive/courses_edited.csv"
        courses=pd.read_csv(url)
        courses.to_csv(path1)
        st.experimental_rerun()

st.subheader("Comments")
if path2.is_file(): 
    comments = pd.read_csv(path2)
    st.write("Comments file already exists ✓", key="comm")
    st.write("Last modified: "+time.ctime(os.path.getctime(path2)))
    st.write("Size: "+str(len(comments)))

    if st.button("Update", key="commUP"):
        url="https://marcolg.altervista.org/drive/comments_edited.csv"
        comments=pd.read_csv(url)
        comments.to_csv(path2)
        st.experimental_rerun()

else:
    st.write("Comments file doesn't exists ✗")
    if st.button("Download"):
        url="https://marcolg.altervista.org/drive/comments_edited.csv"
        comments=pd.read_csv(url)
        comments.to_csv(path2)
        st.write("File created now ✓")
        st.experimental_rerun()
