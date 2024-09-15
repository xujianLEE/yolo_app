import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image 

# 加载模型
def load_model(model_name):
    return YOLO(f"models/{model_name}")

# 处理图像并进行目标检测
#def process_image(file, model, confidence_threshold):
#    img = Image.open(file.stream)
#    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#    results = model(img_cv, conf=confidence_threshold)
#    return img_cv, results
def process_image(file, model, confidence_threshold):
    if isinstance(file, np.ndarray):
        # 如果输入是 numpy 数组（视频帧），直接使用
        img_cv = file
    else:
        # 如果输入是文件对象（上传的图片），按原来的方式处理
        img = Image.open(file.stream)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # 使用模型进行预测
    results = model(img_cv, conf=confidence_threshold)
    
    return img_cv, results
# 提取“person”类别的边界框和置信度
def extract_person_boxes(results):
    person_boxes = []
    for r in results:
        for box in r.boxes:
            if box.cls.item() == 0:  # 0是“person”的类别索引
                person_boxes.append((box.xyxy[0], box.conf.item()))  # 获取边界框坐标和置信度
    return person_boxes

# 在图像上绘制检测结果
def draw_boxes(img_cv, person_boxes):
    for box, conf in person_boxes:
        x1, y1, x2, y2 = map(int, box)
        # 使用红色 (0, 0, 255) 绘制边界框，线条宽度设为 3
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 0, 255), 3)
        # 使用红色绘制文本，字体大小设为 0.7，线条宽度设为 2
        cv2.putText(img_cv, f"person {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)