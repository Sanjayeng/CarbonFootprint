from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity   # keep as you have
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io




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
    core_prefill = ""
    core_id = request.GET.get("core_id")  # coming from core page

    if core_id:
        try:
            core_prefill = Core.objects.get(id=core_id).company_name
        except:
            core_prefill = ""

    if request.method == 'POST':
        Activity.objects.create(
            core=request.POST.get('core'),
            category=request.POST.get('category'),
            value=request.POST.get('value'),
            date=request.POST.get('date'),
        )
        return redirect('emission_index')

    return render(request, 'emissions/add.html', {"core_prefill": core_prefill})


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

def emission_graph(request):
    activities = Activity.objects.all().order_by('date')

    labels = []
    data = []

    for a in activities:
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

        co2 = val * factor if factor else 0
        labels.append(str(a.date))
        data.append(round(co2, 4))

    return render(request, "emissions/graph.html", {
        "labels": labels,   # don't convert to JSON
        "data": data,       # don't convert to JSON
    })

def emission_report_pdf(request):
    activities = Activity.objects.all().order_by('-date')

    rows = []
    for a in activities:
        cat = (a.category or "").lower()
        val = float(a.value)

        if cat in ["electric", "electricity"]:
            factor = 0.000475
        elif cat == "fuel":
            factor = 0.00268
        elif cat == "travel":
            factor = 0.00021
            # you can add more categories if you want
        else:
            factor = 0

        co2 = round(val * factor, 4) if factor else 0

        rows.append({
            "id": a.id,
            "core": a.core,
            "category": a.category,
            "value": a.value,
            "date": a.date,
            "co2": co2,
        })

    
    html = render_to_string("emissions/report.html", {"rows": rows})

 
    result = io.BytesIO()
    pdf = pisa.CreatePDF(io.BytesIO(html.encode("utf-8")), dest=result)

    if pdf.err:
        return HttpResponse("Error generating PDF", status=500)

    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="emissions_report.pdf"'
    return response
