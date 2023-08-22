from io import BytesIO
from django.http import HttpResponseNotFound, HttpResponse, FileResponse
from PIL import Image
import os
from django.shortcuts import render


def image_view(request, path):
    file_path = f'/{path}'
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        response = FileResponse(file)
        _, file_extension = os.path.splitext(file_path)
        if file_extension == '.docx':
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    else:
        return HttpResponseNotFound('File not found')
