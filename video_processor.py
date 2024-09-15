<<<<<<< HEAD
import os
import tempfile
import threading
import queue
import cv2
import time
from flask import jsonify, url_for
from model_handler import load_model, process_image, extract_person_boxes, draw_boxes

processed_frames = queue.Queue()
processing_complete = threading.Event()
processing_thread = None

def process_video_request(request):
    global processing_thread
    try:
        if processing_thread and processing_thread.is_alive():
            processing_complete.set()
            processing_thread.join()

        while not processed_frames.empty():
            processed_frames.get()

        file = request.files['file']
        confidence_threshold = float(request.form['confidence'])
        model_name = request.form['model']
        
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, 'temp_video.mp4')
        file.save(video_path)
        
        model = load_model(model_name)

        processing_complete.clear()

        processing_thread = threading.Thread(target=process_video, args=(video_path, model, confidence_threshold))
        processing_thread.start()

        return jsonify({'stream_url': url_for('video_feed_route', _external=True)})
    except Exception as e:
        import traceback
        error_message = str(e)
        stack_trace = traceback.format_exc()
        print(f"Error: {error_message}\n{stack_trace}")
        return jsonify({'error': error_message}), 500

def process_video(video_path, model, confidence_threshold):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration:.2f} seconds")
    
    frames_to_process = min(int(duration * 2), 60)  # 最多处理30秒，每秒2帧
    
    for i in range(frames_to_process):
        if processing_complete.is_set():
            break
        cap.set(cv2.CAP_PROP_POS_MSEC, i * 500)  # 设置读取位置为每0.5秒的帧
        ret, frame = cap.read()
        if not ret:
            break
        
        _, results = process_image(frame, model, confidence_threshold)
        person_boxes = extract_person_boxes(results)
        draw_boxes(frame, person_boxes)
        
        processed_frames.put(frame)
    
    cap.release()
    os.remove(video_path)
    processing_complete.set()

def video_feed():
    while True:
        if not processed_frames.empty():
            frame = processed_frames.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.5)
        elif processing_complete.is_set() and processed_frames.empty():
            break
        else:
=======
import os
import tempfile
import threading
import queue
import cv2
import time
from flask import jsonify, url_for
from model_handler import load_model, process_image, extract_person_boxes, draw_boxes

processed_frames = queue.Queue()
processing_complete = threading.Event()
processing_thread = None

def process_video_request(request):
    global processing_thread
    try:
        if processing_thread and processing_thread.is_alive():
            processing_complete.set()
            processing_thread.join()

        while not processed_frames.empty():
            processed_frames.get()

        file = request.files['file']
        confidence_threshold = float(request.form['confidence'])
        model_name = request.form['model']
        
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, 'temp_video.mp4')
        file.save(video_path)
        
        model = load_model(model_name)

        processing_complete.clear()

        processing_thread = threading.Thread(target=process_video, args=(video_path, model, confidence_threshold))
        processing_thread.start()

        return jsonify({'stream_url': url_for('video_feed_route', _external=True)})
    except Exception as e:
        import traceback
        error_message = str(e)
        stack_trace = traceback.format_exc()
        print(f"Error: {error_message}\n{stack_trace}")
        return jsonify({'error': error_message}), 500

def process_video(video_path, model, confidence_threshold):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration:.2f} seconds")
    
    frames_to_process = min(int(duration * 2), 60)  # 最多处理30秒，每秒2帧
    
    for i in range(frames_to_process):
        if processing_complete.is_set():
            break
        cap.set(cv2.CAP_PROP_POS_MSEC, i * 500)  # 设置读取位置为每0.5秒的帧
        ret, frame = cap.read()
        if not ret:
            break
        
        _, results = process_image(frame, model, confidence_threshold)
        person_boxes = extract_person_boxes(results)
        draw_boxes(frame, person_boxes)
        
        processed_frames.put(frame)
    
    cap.release()
    os.remove(video_path)
    processing_complete.set()

def video_feed():
    while True:
        if not processed_frames.empty():
            frame = processed_frames.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.5)
        elif processing_complete.is_set() and processed_frames.empty():
            break
        else:
>>>>>>> 52d3ad95bf25c9ef6f07e87aee72716bd2234885
            time.sleep(0.1)