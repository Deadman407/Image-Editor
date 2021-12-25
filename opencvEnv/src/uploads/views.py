from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadForm
from .models import Upload

import time

def uploadImage(request):
    form = UploadForm()

    context = {'form': form}

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    
    if Upload.objects.all().count() > 0:
        upload = Upload.objects.latest('created')
        context = {'form': form, 'upload': upload}

        time.sleep(10)
        upload.delete()

    return render(request, 'upload-form.html', context)

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/upload")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
            return response

    raise Http404

