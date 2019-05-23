from .models import Document
from .models import Profile, Service, Post
from .forms import ProfileImportForm
import random

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