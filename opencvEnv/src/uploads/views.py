from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Upload

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
        upload.delete()

    return render(request, 'upload-form.html', context)

