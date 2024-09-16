import os
from flask import jsonify, current_app
from model_handler import load_model, process_image, extract_person_boxes, draw_boxes
import uuid
import cv2
import torch
import tempfile
def process_image_request(request):
    try:
        file = request.files['file']
        confidence_threshold = float(request.form['confidence'])
        model_name = request.form['model']
        
        model = load_model(model_name)
        img_cv, results = process_image(file, model, confidence_threshold)
        person_boxes = extract_person_boxes(results)
        draw_boxes(img_cv, person_boxes)
        
        # 使用相对路径保存临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg', dir='static/temp')
        cv2.imwrite(temp_file.name, img_cv)
        
        # 获取相对路径
        relative_path = os.path.relpath(temp_file.name, 'static')
        
        return jsonify({'result_image_url': f'/static/{relative_path}'})
    except Exception as e:
        print(f"Error in process_image_request: {str(e)}")
        return jsonify({'error': str(e)}), 500