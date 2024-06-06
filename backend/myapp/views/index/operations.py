from .face_processor import FaceProcessor
from rest_framework.decorators import api_view
from myapp.utils import image_to_base64, base64_to_image
from myapp.handler import APIResponse
predictor_path = 'shape_predictor_68_face_landmarks.dat'
processor = FaceProcessor(predictor_path)


@api_view(['POST'])
def thin(request):
    image = request.data['image']
    if(image):
        res = image_to_base64(processor.face_thin(base64_to_image(image)))
        return APIResponse(code=0, msg='操作成功', data={'image': res})
    return APIResponse(code=0, msg='操作失败')

@api_view(['POST'])
def bigeye(request):
    image = request.data['image']
    if(image):
        res = image_to_base64(processor.face_bigeye(base64_to_image(image)))
        return APIResponse(code=0, msg='操作成功', data={'image': res})
    return APIResponse(code=0, msg='操作失败')


@api_view(['POST'])
def smooth(request):
    image = request.data['image']
    if(image):
        res = image_to_base64(processor.face_smooth(base64_to_image(image)))
        return APIResponse(code=0, msg='操作成功', data={'image': res})
    return APIResponse(code=0, msg='操作失败')

@api_view(['POST'])
def whiten(request):
    image = request.data['image']
    if(image):
        res = image_to_base64(processor.face_whiten(base64_to_image(image)))
        return APIResponse(code=0, msg='操作成功', data={'image': res})
    return APIResponse(code=0, msg='操作失败')




