import streamlit as st
import cv2
import numpy as np
#import matplotlib.pyplot as plt


def upload_field():
    # 上传图像
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
       st.image(uploaded_file, caption='Original Image')
       result = cv2.imdecode(np.frombuffer(uploaded_file.read(),np.uint8),cv2.IMREAD_COLOR)
       return result 
    else:
       return None

def oil_painting_effect(img_upload, intensity, quant_level, edge_threshold,edge_effect):
    """
    油画风格转换函数
    参数：
        intensity: 效果强度（推荐5-10）
        quant_level: 颜色量化级别（推荐4-8）
        edge_threshold: 边缘检测阈值（推荐30-100）
    """
    # 读取图片
    img = img_upload
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    # 1. 应用双边滤波（保留边缘的平滑）
    filtered = cv2.bilateralFilter(img, d=intensity, 
                                 sigmaColor=75, 
                                 sigmaSpace=75)
    
    # 2. 颜色量化
    quantized = filtered // quant_level * quant_level
    
    # 3. 边缘检测（增强笔触感）
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, edge_threshold, edge_threshold*2)
    
    # 4. 合成最终效果
    ed = edge_effect
    rt = 1- edge_effect    
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    result = cv2.bitwise_and(quantized, quantized, mask=~edges[:,:,0])   
    result = cv2.addWeighted(result, rt, edges, ed, 0)
    
    return  result


if __name__ == "__main__": 
    st.text("For more image tools, please visite our web ")
    st.page_link("https://www.redpandatail.com", label="www.redpandatail.com", icon="🌎")
    img_upload = upload_field()
    if img_upload is not None: 
        intensity= st.slider(label=' intensity',
                                     min_value = 1,
                                     max_value= 200,
                                     value = 7,
                                    )
        quant_level = st.slider(label='color_level ',
                                       min_value = 1,
                                       max_value = 100,
                                       value = 1,
                                       )  
        
        edge_threshold = st.slider(label='edge_threshold',
                                       min_value = 0,
                                       max_value = 200,
                                       value = 55,
                                       ) 
        edge_effect = st.slider(label='edge_effect',
                                       min_value = 0.0,
                                       max_value = 0.5,
                                       value = 0.1,
                                       ) 
        

        oil_painting = oil_painting_effect(img_upload, intensity, quant_level,edge_threshold,edge_effect)

        st.image(oil_painting, caption='Output Image')
