from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls')),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('imageconvert/', include('imageconvert.urls', namespace='imageconvert')),
    path('goods/', include('goods.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
