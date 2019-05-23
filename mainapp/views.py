import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
# from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, PostPhoto, Tag, Category, Document, Article, Message, Contact
from .models import Registry, Menu, Profile, Service
from .models import Staff
from .forms import PostForm, ArticleForm, DocumentForm, ProfileImportForm
from .forms import SendMessageForm, SubscribeForm, AskQuestionForm, SearchRegistryForm
from .adapters import MessageModelAdapter
from .message_tracker import MessageTracker
from .utilites import UrlMaker, update_from_dict
from .registry_import import Importer, data_url

# Create your views here.

def index(request):
    #TODO:  сделать когда-нибудь вывод форм на глваную
    title = 'Главная страница'
    """this is mainpage view with forms handler and adapter to messages"""
    # tracker = MessageTracker()
    if request.method == 'POST':
        request_to_dict = dict(zip(request.POST.keys(), request.POST.values()))
        form_select = {
            'send_message_button': SendMessageForm,
            'subscribe_button': SubscribeForm,
            'ask_question': AskQuestionForm,
        }
        for key in form_select.keys():
            if key in request_to_dict:
                print('got you!', key)
                form_class = form_select[key]
        form = form_class(request_to_dict)
        if form.is_valid():

            # saving form data to messages (need to be cleaned in future)
            adapted_data = MessageModelAdapter(request_to_dict)
            adapted_data.save_to_message()
            print('adapted data saved to database')
            tracker.check_messages()
            tracker.notify_observers()
        else:
            raise ValidationError('form not valid')

    from .models import CenterPhotos

    content = {
        'title': title,
        'center_photos': CenterPhotos.objects.all().order_by('number')

        # 'docs': docs,
        # 'articles': main_page_articles,
        # 'send_message_form': SendMessageForm(),
        # 'subscribe_form': SubscribeForm(),
        # 'ask_question_form': AskQuestionForm()
    }

    return render(request, 'mainapp/index.html', content)

def reestr(request):
    title = 'Реестр'

    content = {
        'title': title
    }
    return render(request, 'mainapp/reestr.html', content)


def doc(request):
    from .models import DocumentCategory

    content={
        "title": "Документы",
        'docs': Document.objects.all(),
        'categories': DocumentCategory.objects.all()
    }
    return render(request, 'mainapp/doc.html', content)

def partners(request):
    return render(request, 'mainapp/partners.html')

def page_details(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    side_panel = post.side_panel
    # service = get_object_or_404(Service, pk=pk)
    content = {
        'title': 'Детальный просмотр',
        'post': post,
        'side_panel': side_panel
    }
    return render(request, 'mainapp/page_details.html', content)

def service_details(request, pk=None):
    service = get_object_or_404(Service, pk=pk)
    content = {
        'title': 'Детальный просмотр',
        'post': service,
    }
    return render(request, 'mainapp/page_details.html', content)

def cok(request):
    spks_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="НПА СПКС")
    ).order_by('-created_date')
    spks_example_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="Образцы документов СПКС")
    )
    content = {
        'title': 'cok_documets',
        'spks_documents': spks_documents,
        'spks_example_documents': spks_example_documents
    }
    return render(request, 'mainapp/cok.html', content)

def profstandarti(request):
    from .models import Profstandard
    profstandards = Profstandard.objects.all().order_by('number')
    content = {
        'title': 'Профессиональные стандарты',
        'profstandards': profstandards,
    }
    return render(request, 'mainapp/profstandarti.html', content)
def contacts(request):
    content = {
        'title': 'Контакты',
        'contacts': Contact.objects.all().order_by('number')
    }
    return render(request, 'mainapp/contacts.html', content)
def all_news(request):
    content = {
        'title': 'All news',
        'news': Post.objects.all().order_by('-published_date')[:9]
    }
    return render(request, 'mainapp/all_news.html', content)

def political(request):
    political_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="НПА СПКС")
    ).order_by('-created_date')
    political_example_documents = Document.objects.filter(
        tags__in=Tag.objects.filter(name="Образцы документов СПКС")
    )
    content = {
        'title': 'political_documets',
        'political_documents': political_documents,
        'political_example_documents': political_example_documents
    }
    return render(request, 'mainapp/political.html', content)

def details_news(request, pk=None):

    return_link = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(publish_on_news_page=True).exclude(pk=pk)[:3]
    attached_images = PostPhoto.objects.filter(post__pk=pk)
    attached_documents = Document.objects.filter(post__pk=pk)
    post_content = {
        'post': post,
        'related_posts': related_posts,
        'images': attached_images,
        'documents': attached_documents,
    }

    return render(request, 'mainapp/details_news.html', post_content)

def import_profile(request):
    content = {}
    if request.method == "POST":
        if len(request.FILES) > 0:
            form = ProfileImportForm(request.POST, request.FILES)
            if form.is_valid():
                data = request.FILES.get('file')
                file = data.readlines()
                import_data = {}
                for line in file:
                    string = line.decode('utf-8')
                    if string.startswith('#') or string.startswith('\n'):
                        # print('Пропускаем: ', string)
                        continue
                    splitted = string.split("::")
                    import_data.update({splitted[0].strip(): splitted[1].strip()})
                    # print('Импортируем:', string)
                profile = Profile.objects.first()
                if profile is None:
                    profile = Profile.objects.create(org_short_name="DEMO")
                try:
                    #updating existing record with imported fields
                    update_from_dict(profile, import_data)
                    content.update({'profile_dict': '{}'.format(profile.__dict__)})
                    content.update({'profile': profile})
                    print('***imported***')
                except Exception as e:
                    print("***ERRORS***", e)
                    content.update({'errors': e})
        else:
            content.update({'errors': 'Файл для загрузки не выбран'})
        return render(request, 'mainapp/includes/profile_load.html', content)
