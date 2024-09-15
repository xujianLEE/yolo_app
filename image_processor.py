import os
from flask import jsonify, current_app
from model_handler import load_model, process_image, extract_person_boxes, draw_boxes
import uuid
import cv2

def process_image_request(request):
    try:
        file = request.files['file']
        confidence_threshold = float(request.form['confidence'])
        model_name = request.form['model']
        
        model = load_model(model_name)
        img_cv, results = process_image(file, model, confidence_threshold)
        person_boxes = extract_person_boxes(results)
        draw_boxes(img_cv, person_boxes)

        # 生成唯一的文件名
        unique_filename = f"result_image_{uuid.uuid4().hex}.png"
        output_path = os.path.join(current_app.static_folder, unique_filename)
        
        print(f"Saving image to: {output_path}")
        cv2.imwrite(output_path, img_cv)

        if os.path.exists(output_path):
            print(f"File exists: {output_path}")
            file_size = os.path.getsize(output_path)
            print(f"File size: {file_size} bytes")
        else:
            print(f"File does not exist: {output_path}")

        result_url = f'/static/{unique_filename}'
        print(f"Result URL: {result_url}")

        return jsonify({'result_image_url': result_url})
    except Exception as e:
        print(f"Error in process_image_request: {str(e)}")
        return jsonify({'error': str(e)}), 500