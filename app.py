import os
from flask import Flask, send_from_directory
from routes import register_routes
from utils import get_local_ip

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置静态文件夹的路径
static_folder = os.path.join(current_dir, 'static')

app = Flask(__name__, static_folder=static_folder, static_url_path='/static')


# 确保静态文件夹存在
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

# 添加一个路由来处理静态文件
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(static_folder, filename)

register_routes(app)

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"应用运行在: http://{local_ip}:5000")
    print(f"静态文件夹路径: {static_folder}")
    app.run(host='0.0.0.0', port=5000, debug=True)