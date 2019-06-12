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

    #render self templet with self context
    # def render(self):
    #     return self.template.render(self.context)

from .models import Document

def random_documents(request):
    all_documents = Document.objects.all()
    if len(all_documents) > 3:
        all_document_pks = [doc.pk for doc in all_documents]
        documents = []
        for i in range(0, 5):
            try:
                random_document = Document.objects.get(pk=random.choice(all_document_pks))
                # import pdb; pdb.set_trace()
                if random_document not in documents:
                    documents.append(random_document)
            except Exception as e:
                return {'random_documents': [e]}
        return {'random_documents': documents}
    else:
        return {'random_documents': ['Добавьте больше документов в базу данных']}

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
    components = Component.objects.filter(configuration=site)
    # import pdb; pdb.set_trace()
    return {
            'site': {
                'components': components
                }
            }

def site_components(request):
    site_components = Component.objects.all().order_by('number')
    components = {}
    for c in site_components:
        component = SiteComponent(c.html, c.contxt)
        components.update({c.code: component})
    return {'components': components}