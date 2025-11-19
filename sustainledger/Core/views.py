from django.shortcuts import render, redirect
from .models import Core, Facility
from django.contrib.auth.decorators import login_required



# CORE ADD
@login_required
def core_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        Core.objects.create(name=name, location=location)
        return redirect('Core:core_list')

    return render(request, "Core/core_add.html")


# CORE LIST
@login_required
def core_list(request):
    cores = Core.objects.all()
    return render(request, "Core/core_list.html", {"cores": cores})


# FACILITY ADD

@login_required
def facility_add(request):
    cores = Core.objects.all()

    if request.method == "POST":
        core_id = request.POST.get("core")
        name = request.POST.get("name")
        location = request.POST.get("location")

        Facility.objects.create(
            core_id=core_id,
            name=name,
            location=location
        )
        return redirect('Core:facility_list')

    return render(request, "Core/facility_add.html", {"cores": cores})


# FACILITY LIST
@login_required
def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, "Core/facility_list.html", {"facilities": facilities})
