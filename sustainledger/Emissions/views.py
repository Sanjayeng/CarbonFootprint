from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity   # keep as you have



def emission_index(request):
    activities = Activity.objects.all().order_by('-date')

    rows = []
    for a in activities:
        # simple Python-side CO2 calculation
        cat = (a.category or "").lower()
        val = float(a.value)

        if cat in ["electric", "electricity"]:
            factor = 0.000475     
        elif cat == "fuel":
            factor = 0.00268      
        elif cat == "travel":
            factor = 0.00021       
        else:
            factor = 0

        co2 = None
        if factor != 0:
            co2 = round(val * factor, 4)

        rows.append({
            "id": a.id,
            "core": a.core,
            "category": a.category,
            "value": a.value,
            "date": a.date,
            "co2": co2,
        })

    return render(request, "emissions/index.html", {"rows": rows})


def activity_add(request):
    if request.method == "POST":
        Activity.objects.create(
            core=request.POST.get("core"),
            category=request.POST.get("category"),
            value=request.POST.get("value"),
            date=request.POST.get("date"),
        )
        return redirect("emission_index")

    return render(request, "emissions/add.html")

def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    if request.method == "POST":
        activity.core = request.POST.get("core")
        activity.category = request.POST.get("category")
        activity.value = request.POST.get("value")
        activity.date = request.POST.get("date")
        activity.save()
        return redirect("emission_index")

    return render(request, "emissions/edit.html", {"activity": activity})


def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity.delete()
    return redirect("emission_index")
