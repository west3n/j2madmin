from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('balance/', views.balance_view, name='balance'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('info/', views.info_view, name='info'),
    path('partners/', views.partners_view, name='partners'),
    path('support/', views.support_view, name='support'),
    path('admin/', admin.site.urls),
    path('files/<path:path>', views.image_view, name='file_view')
]
