from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('main.urls')),
    path('mydesign/', views.mydesign),
]
=======
    path('', include('goods.urls')),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> 95c81fba387f12fc5381d12d05df40292731ddb9
