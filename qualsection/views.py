from django.shortcuts import render
from .models import *
# Create your views here.


def main(request):
    cok_place = CokPlaceInfo.objects.first()
    cok_contacts = CokContact.objects.first()
    profstandards = CokProfstandard.objects.all().order_by('number')
    profqualifications = []
    for ps in profstandards:
        profqualifications.append({
            "profstandard": ps,
            "qualifications": CokQualification.objects.filter(profstandard=ps, active=True).order_by('number')
        })

    cok_exam_places = CokQualExamPlace.objects.all().order_by('number')
    cok_zayavki = {
        "zayavka_1": CokDocument.objects.filter(pseudo="zayavka_1").first(),
        "zayavka_2": CokDocument.objects.filter(pseudo="zayavka_2").first()
    }
    pravila = CokDocument.objects.filter(pseudo="pravila").first()
    # import pdb; pdb.set_trace()
    content = {
        "cok_place": cok_place,
        "cok_contacts": cok_contacts,
        "profqualifications": profqualifications,
        "cok_exam_places": cok_exam_places,
        "cok_zayavki": cok_zayavki,
        "pravila": pravila
    }
    return render(request, 'qualsection/main_template.html', content)