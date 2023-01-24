import streamlit as st
import backend as be
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

be.style()

st.header("Courses summary")

st.write("Brief insight on what should you want to learn given what we can discover using the exploration of our dataset")

categories=be.stats()

print(categories.info())

st.write(categories.plot())