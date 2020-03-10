from django.contrib import admin
from .models import *
# import pdb; pdb.set_trace()

class CokQualificationInline(admin.TabularInline):
    model = CokQualification
    extra = 0

@admin.register(CokQualification)
class CokQualificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'pseudo', 'number', 'get_documents_number', 'active']


    def get_documents_number(self, obj):
        return len([d for d in obj.documents.all()])

    get_documents_number.short_description = 'Кол-во документов'

@admin.register(CokDocument)
class CokDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'pseudo', 'number']



@admin.register(CokProfstandard)
class AdminCokProfstandard(admin.ModelAdmin):
    list_display = ['title', 'number']

    inlines = [
        CokQualificationInline,
    ]

# Register your models here.
admin.site.register(CokPlaceInfo)
admin.site.register(CokContact)
# admin.site.register(CokDocument)
admin.site.register(CokQualExamPlace)