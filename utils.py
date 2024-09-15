import os
import socket
import base64
import io
from PIL import Image

# 获取models文件夹中的所有.pt文件
def get_model_files():
    model_dir = 'models'
    return [f for f in os.listdir(model_dir) if f.endswith('.pt')]

# 获取本机IP地址
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# 将图像转换为Base64编码
def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')