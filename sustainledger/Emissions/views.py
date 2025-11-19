from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity   # keep as you have
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
from Core.models import Facility



def emission_index(request, facility_id=None):
    """
    If facility_id is provided, show only that facility's emissions.
    If not provided, show all emissions.
    """

    # If filtering by facility
    if facility_id is not None:
        facility = get_object_or_404(Facility, id=facility_id)
        activities = Activity.objects.filter(facility=facility).order_by('-date')

        # Build rows for template
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
            else:
                factor = 0

            co2 = round(val * factor, 4) if factor else None

            rows.append({
                "id": a.id,
                "facility": a.facility.name,
                "category": a.category,
                "value": a.value,
                "date": a.date,
                "co2": co2,
            })

        return render(request, "emissions/index.html", {
            "rows": rows,
            "facility": facility,
        })

    # If no facility_id → show all activities
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
        else:
            factor = 0

        co2 = round(val * factor, 4) if factor else None

        rows.append({
            "id": a.id,
            "facility": a.facility.name,
            "category": a.category,
            "value": a.value,
            "date": a.date,
            "co2": co2,
        })

    return render(request, "emissions/index.html", {"rows": rows})

def activity_add(request):
    facility_prefill = ""
    facility_id = request.GET.get("facility_id")   # coming from facility list

    # Pre-fill facility name in the form
    if facility_id:
        try:
            facility_prefill = Facility.objects.get(id=facility_id).name
        except Facility.DoesNotExist:
            facility_prefill = ""

    if request.method == 'POST':
        facility_obj = Facility.objects.get(id=request.POST.get('facility_id'))

        Activity.objects.create(
            facility=facility_obj,
            category=request.POST.get('category'),
            value=request.POST.get('value'),
            date=request.POST.get('date'),
        )
        return redirect('emissions:emission_index', facility_id=facility_obj.id)


    return render(request, 'emissions/add.html', {
        "facility_prefill": facility_prefill,
        "facility_id": facility_id
    })
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)

    facilities = Facility.objects.all()  # MUST BE HERE

    if request.method == "POST":
        print("POST DATA:", request.POST)


        facility_id = request.POST.get("facility_id")
        if not facility_id:
            return HttpResponse("Facility ID missing in form POST", status=400)

        facility_obj = get_object_or_404(Facility, id=facility_id)

        activity.facility = facility_obj
        activity.category = request.POST.get("category")
        activity.value = request.POST.get("value")
        activity.date = request.POST.get("date")
        activity.save()

        return redirect("emissions:emission_index", facility_id=facility_obj.id)

    return render(request, "emissions/edit.html", {
        "activity": activity,
        "facilities": facilities,
    })





def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    facility_id = activity.facility.id
    activity.delete()

    return redirect("emissions:emission_index", facility_id=facility_id)


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

