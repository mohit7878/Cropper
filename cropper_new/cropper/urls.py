from django.urls import path
from cropper import views

app_name = 'cropper'

urlpatterns = [
    path('cropper_main/', views.cropper_main, name='cropper_main')
]
