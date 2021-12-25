from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from uploads.views import uploadImage
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', uploadImage, name='upload_image'),
    url(r'^download/(?P<path>.*)$',serve,{'document.root':settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)