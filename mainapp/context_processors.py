from .models import Document
from .models import Profile, Service, Post, SiteConfiguration, Component
from .forms import ProfileImportForm
import random
from django.template import Context, Template
from django.shortcuts import render, get_object_or_404

class SiteComponent:
    def __init__(self, html, contxt, css_file):
        self.template = Template(html)
        self.context = Context(contxt)
        self.css = css_file

    def render(self):
        return self.template.render(self.context)

def random_documents(request):
    all_documents = Document.objects.all()
    if len(all_documents) > 2:
        all_document_pks = [doc.pk for doc in all_documents]
        documents = [Document.objects.get(pk=random.choice(all_document_pks)) for i in range(0, 3)]
        return {'random_documents': documents}
    else:
        return {'random_documents': ['Нет документов в базе данных']}

def basement_news(request):
    basement_news = Post.objects.filter(publish_on_main_page=True).order_by('-published_date')[:3]
    return {'basement_news': basement_news}

def profile_chunks(request):
    profile = Profile.objects.first()
    return {'profile': profile}

def services(request):
    all_services = Service.objects.all().order_by('number')
    return {'all_services': all_services}

def profile_import(request):
    profile_import_form = ProfileImportForm()
    return {'profile_import_form': profile_import_form}

def site_configuration(request):
    site = SiteConfiguration.objects.first()
    return {'site': site}

def site_components(request):
    site_components = Component.objects.all().order_by('number')
    components = {}
    for c in site_components:
        component = SiteComponent(c.html, c.contxt)
        components.update({c.code: component})
    return {'components': components}