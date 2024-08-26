import streamlit as st
from Home import face_rec
from streamlit_webrtc import webrtc_streamer
import av
import time


st.set_page_config(page_title='Predictions',layout='centered')
st.subheader('Real-Time Attendance System')


# Retrive the data from Redis Database
with st.spinner('Retriving Data from Redis Database...'):
    redis_face_db = face_rec.retrive_data(name='academy:register')
    st.dataframe(redis_face_db)

st.success("Data successfully retrived from Redis")    
# time
waitTime = 30  # time in sec
setTime = time.time()
realtimepred = face_rec.RealTimePred()  # real time prediction class

# Real Time Prediction
# streamlit webrtc

# callback function
def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24")  # 3D numpy array
    # operation that you can perform on the array
    pred_img = realtimepred.face_prediction(img,redis_face_db,'Facial Features',['Name','Role'],thresh=0.5)

    timenow = time.time()
    difftime = timenow - setTime
    if difftime >= waitTime:
        realtimepred.saveLogs_redis()
        setTime = time.time() # reset time
        print('Save data to Redis Database')
    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimePrediction", video_frame_callback=video_frame_callback)