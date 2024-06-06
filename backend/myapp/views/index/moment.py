# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Moment
from myapp.serializers import MomentSerializer
from myapp.utils import dict_fetchall


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        sort = request.GET.get("sort", 'recent')

        # 排序方式
        order = '-create_time'
        if sort == 'recent':
            order = '-create_time'
        elif sort == 'hot' or sort == 'recommend':
            order = '-pv'
        Moments = Moment.objects.all().order_by(order)

        serializer = MomentSerializer(Moments, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)

@api_view(['POST'])
def create(request):
    serializer = MomentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='创建失败')

