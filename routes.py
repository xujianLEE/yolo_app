from flask import render_template, request, jsonify, Response, url_for
from image_processor import process_image_request
from video_processor import process_video_request, video_feed
from utils import get_model_files

def register_routes(app):
    @app.route('/')
    def index():
        model_files = get_model_files()
        return render_template('index.html', model_files=model_files)

    @app.route('/detect_image', methods=['POST'])
    def detect_image():
        return process_image_request(request)

    @app.route('/detect_video', methods=['POST'])
    def detect_video():
        return process_video_request(request)

    @app.route('/video_feed')
    def video_feed_route():
        return Response(video_feed(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')