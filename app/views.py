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


def home(request):
    return render(request, 'home/home.html')


def balance_view():
    pass


def deposit_view():
    pass


def withdraw_view():
    pass


def info_view():
    pass


def partners_view():
    pass


def support_view():
    pass
