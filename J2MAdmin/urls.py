from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/<path:path>', views.image_view, name='file_view')
]
