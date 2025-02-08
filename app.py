import streamlit as st
import cv2
import numpy as np
from PIL import Image


iniv_sigma_s_v=0
iniv_sigma_r_v=0

# 上传图像
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
 img_cv=cv2.imdecode(np.frombuffer(uploaded_file.read(),np.uint8),cv2.IMREAD_COLOR)

sigma_s_v = st.slider(label='sigma_s',
                             min_value = 0.0,
                             max_value= 100.0,
                             value = 30.0,
                             )

sigma_r_v = st.slider(label='sigma_r',
                             min_value = 0.0,
                             max_value = 10.0,
                             value = 1.5,
                             )


# 图像水彩画效果处理
def stylization(img,sigma_s_v,sigma_r_v):
    result = cv2.stylization(img,sigma_s=sigma_s_v,sigma_r = sigma_r_v)
    return result

if sigma_s_v != iniv_sigma_r_v or sigma_r_v != iniv_sigma_r_v:
    img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_processed = stylization(img,sigma_s_v,sigma_r_v)
    progress_bar = st.empty()
    for i in range(10):
          progress_bar.progress(i/9, 'Processing, please wait...')
          time.sleep(1)

    st.image(Sketch, caption="edged Image", use_container_width=True)
    iniv_sigma_s_v=sigma_s_v
    iniv_sigma_r_v=sigma_r_v
