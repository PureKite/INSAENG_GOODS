from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'imageconvert'

urlpatterns = [
    path('', views.imageconvert),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)