from django.shortcuts import redirect, render

from .models import Activity

# Create your views here.
def emission_index(request):
    activities = Activity.objects.all()
    return render(request, 'Emissions/index.html', {'activities': activities})

def activity_add(request):
    if request.method == 'POST':
        core = request.POST.get('core')
        category = request.POST.get('category')
        value = request.POST.get('value')
        date = request.POST.get('date')

        Activity.objects.create(
            core=core,
            category=category,
            value=value,
            date=date
        )

        return redirect('emissions_index')

    return render(request, 'emissions/add.html')
    