import streamlit as st
import cv2
import numpy as np
import time


st.text("For more image tools, please visite our website ")
st.page_link("https://www.redpandatail.com", label="www.redpandatail.com", icon="🌎")

def upload_field():
    # 上传图像
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
       st.image(uploaded_file, caption='Original Image')
       result = cv2.imdecode(np.frombuffer(uploaded_file.read(),np.uint8),cv2.IMREAD_COLOR)
       return result 
    else:
       return None

# 程序的主要逻辑
def skin_process(img_file, effect):
    image=img_file
    step = 2
    pw=effect/10
    # 图片大一点，此处尺寸大一点
    kernel = (16, 16) 
    image = image / 255
    image_size = image.shape[:2]
    # round() 方法返回浮点数x的四舍五入值
    source_size = (int(round(image_size[1] * step)), int(round(image_size[0] * step)))
    target_size = (int(round(kernel[0] * step*pw)), int(round(kernel[0] * step*pw)))
    print(target_size)
    # cv2.resize() 方法对图片进行缩放，插值方法: 双线性插值（默认设置）
    sI = cv2.resize(image, source_size, interpolation=cv2.INTER_LINEAR)
    sp = cv2.resize(image, source_size, interpolation=cv2.INTER_LINEAR)
    # cv2.blur() 方法对图像进行均值滤波
    msI = cv2.blur(sI, target_size)
    msp = cv2.blur(sp, target_size)
    msII = cv2.blur(sI * sI, target_size)
    msIp = cv2.blur(sI * sp, target_size)
    vsI = msII - msI * msI
    csIp = msIp - msI * msp
    recA = csIp / (vsI + 0.01)
    recB = msp - recA * msI
    mA = cv2.resize(recA, (image_size[1], image_size[0]), interpolation=cv2.INTER_LINEAR)
    mB = cv2.resize(recB, (image_size[1], image_size[0]), interpolation=cv2.INTER_LINEAR)
    gf = mA * image + mB
    gf = gf * 255
    gf[gf > 255] = 255
    # astype() 方法进行强制类型转换
    final = gf.astype(np.uint8)
    return final



#定义锐化滤波器增加亮度
def img_sharpen(img_process,contrast,brightness):
    img=img_process
    alpha = brightness
    beta = contrast
    sharpen_filter = np.array([[0,-1,0],
                                           [-1,3,-1],
                                           [0,1,0]])    
    
    # 亮度增加50，对比度增加1.5
    sharpened_image = cv2.filter2D(img, -1, sharpen_filter)
    adjusted = cv2.convertScaleAbs(sharpened_image, alpha=alpha, beta=beta)
    return adjusted 


if __name__ == "__main__": 
    img_upload = upload_field()
    if img_upload is not None:        
        effect= st.slider(label='effect',
                                     min_value = 1,
                                     max_value= 10,
                                     value = 4,
                                    )
        img_process=skin_process(img_upload, effect)
        contrast= st.slider(label='contrast',
                                     min_value = 0.0,
                                     max_value= 50.0,
                                     value = 1.2,
                                    )
        brightness = st.slider(label='brightness',
                                       min_value = 0.0,
                                       max_value = 5.0,
                                       value = 1.6,
                                       )
        img_sharpen=img_sharpen(img_process,contrast,brightness )
        img = cv2.cvtColor(img_sharpen, cv2.COLOR_BGR2RGB)
        st.image(img, caption='Output Image')
