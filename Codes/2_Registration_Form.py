import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av


st.set_page_config(page_title='Registration Form',layout='centered')
st.subheader('Registration Form')

# step-1: Collect person name and role
# form
person_name = st.text_input(label='Name')