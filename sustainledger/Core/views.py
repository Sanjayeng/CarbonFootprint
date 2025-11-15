from urllib import request
from django.shortcuts import redirect, render
from .models import core
# Create your views here.

  

def index(request):
    core_objects = core.objects.all()
    data = {'core_list': core_objects}
    return render(request, 'Core/index.html', data)

def add_core(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        new_core = core(name=name, location=location)
        new_core.save()

        return redirect('Core:index')

    return render(request, 'Core/add.html')
    
   