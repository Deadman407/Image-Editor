from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from uploads.views import uploadImage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', uploadImage, name='upload_image'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)