from django.shortcuts import render, redirect
from .models import Activity  


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
