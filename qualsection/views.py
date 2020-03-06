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
            "qualifications": CokQualification.objects.filter(profstandard=ps).order_by('number')
        })
    # import pdb; pdb.set_trace()
    content = {
        "cok_place": cok_place,
        "cok_contacts": cok_contacts,
        "profqualifications": profqualifications,
    }
    return render(request, 'qualsection/main_template.html', content)