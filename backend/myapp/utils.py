import datetime
import hashlib

from rest_framework.views import exception_handler

from myapp.serializers import ErrorLogSerializer
import numpy as np
import cv2
import base64

def md5value(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    md5str = (input_name.hexdigest()).lower()
    print('计算md5:', md5str)
    return md5str


def dict_fetchall(cursor):  # cursor是执行sql_str后的记录，作入参
    columns = [col[0] for col in cursor.description]  # 得到域的名字col[0]，组成List
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def get_ip(request):
    """
    获取请求者的IP信息
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_ua(request):
    """
    获取请求者的IP信息
    """
    ua = request.META.get('HTTP_USER_AGENT')
    return ua[0:200]


def getWeekDays():
    """
    获取近一周的日期
    """
    week_days = []
    now = datetime.datetime.now()
    for i in range(7):
        day = now - datetime.timedelta(days=i)
        week_days.append(day.strftime('%Y-%m-%d %H:%M:%S.%f')[:10])
    week_days.reverse()  # 逆序
    return week_days


def get_monday():
    """
    获取本周周一日期
    """
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(now.weekday())
    return monday.strftime('%Y-%m-%d %H:%M:%S.%f')[:10]


def log_error(request, content):
    """
    记录错误日志
    """
    ip = get_ip(request)
    method = request.method
    url = request.path

    data = {
        'ip': ip,
        'method': method,
        'url': url,
        'content': content
    }

    # 入库
    serializer = ErrorLogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

#base64解码
def image_to_base64(image):
    # 将图像编码成内存缓冲区
    _, buffer = cv2.imencode('.jpg', image)
    
    # 将缓冲区内容转换成 Base64 字符串
    base64_str = base64.b64encode(buffer).decode('utf-8')
    base64_str='data:image/jpeg;base64,' + base64_str
    return base64_str

def base64_to_image(base64_string):
    base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    
    # 将二进制数据转换成 NumPy 数组
    np_arr = np.frombuffer(image_data, np.uint8)
    
    # 解码成图像
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # 如果是灰度图，使用 cv2.IMREAD_GRAYSCALE
    
    return image
