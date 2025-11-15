from django.shortcuts import render

# Create your views here.
def activitylist(request):
    return render(request, 'Emissions/activitylist.html')