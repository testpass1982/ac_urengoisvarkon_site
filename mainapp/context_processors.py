from .models import Document
from .models import Profile, Service, Post, SiteConfiguration, Component
from .forms import ProfileImportForm
import random
from django.template import Context, Template
from django.shortcuts import render, get_object_or_404
from .models import Document
from django.utils.termcolors import colorize
from .classes import SiteComponent


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
    basement_news = Post.objects.filter(
        publish_on_main_page=True).order_by(
            '-published_date')[:3]
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
    # import pdb; pdb.set_trace()
    try:
        site = SiteConfiguration.objects.filter(activated=True)
        bd_components = Component.objects.filter(configuration=site[0].pk).order_by('number')
        site_components = [SiteComponent(component) for component in bd_components]
        # import pdb; pdb.set_trace()
        return {
                'site': {
                    'components': site_components,
                    }
                }
    except Exception as e:
        print (colorize('###---> SITE CONFIGURATION ERROR: {}'.format(e), bg='red'))
        return {'site': {'components': None}}
