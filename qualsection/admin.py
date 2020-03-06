from django.contrib import admin
from .models import *
# import pdb; pdb.set_trace()

class CokQualificationInline(admin.TabularInline):
    model = CokQualification
    extra = 0

@admin.register(CokProfstandard)
class AdminCokProfstandard(admin.ModelAdmin):
    list_display = ['title', 'number']

    inlines = [
        CokQualificationInline,
    ]

# Register your models here.
admin.site.register(CokPlaceInfo)
admin.site.register(CokContact)
admin.site.register(CokDocument)
# admin.site.register(CokProfstandard)
admin.site.register(CokQualification)
admin.site.register(CokQualExamPlace)