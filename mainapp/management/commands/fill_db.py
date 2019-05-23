# core import file
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.core.files import File
from mainapp.models import Menu, Post, Article, PostPhoto, Tag, Category, Chunk
from mainapp.models import Contact, Document, Profile, DocumentCategory, Service, CenterPhotos
from mainapp.models import Attestat
from django.conf import settings
from mixer.backend.django import mixer
import random
from django.conf import settings
from django.utils import timezone
import os, shutil

# from model_mommy.recipe import Recipe, foreign_key, seq

# clean upload folder
if os.path.isdir(os.path.join(settings.BASE_DIR, 'media', 'upload')):
    folder = os.path.join(settings.BASE_DIR, 'media', 'upload')
    for a_file in os.listdir(folder):
        a_file_path = os.path.join(folder, a_file)
        try:
            if os.path.isfile(a_file_path):
                os.unlink(a_file_path)
        except Exception as e:
            print('ERROR', e)
# import pdb; pdb.set_trace()

#clean upload/media folder
if os.path.isdir(os.path.join(settings.BASE_DIR, 'media', 'upload', 'media')):
    media_folder = os.path.join(settings.BASE_DIR, 'media', 'upload', 'media')
    for a_file in os.listdir(media_folder):
        # print(a_file)
        a_file_path = os.path.join(media_folder, a_file)
        try:
            if os.path.isfile(a_file_path):
                os.unlink(a_file_path)
        except Exception as e:
            print('ERROR', e)

#clean media/documents/ folder
if os.path.isdir(os.path.join(settings.BASE_DIR, 'media', 'documents', 'media')):
    documents_folder = os.path.join(settings.BASE_DIR, 'media', 'documents', 'media')
    for a_file in os.listdir(documents_folder):
        # print(a_file)
        a_file_path = os.path.join(documents_folder, a_file)
        try:
            if os.path.isfile(a_file_path):
                os.unlink(a_file_path)
        except Exception as e:
            print('ERROR', e)

images = [
    'media/01.JPG',
    'media/02.JPG',
    'media/03.JPG',
    'media/04.JPG',
    'media/05.JPG',
    'media/06.JPG',
]

attestats = [
    'media/sv_1.jpg',
    'media/sv_2.jpg',
    'media/sv_3.jpg',
    'media/sv_4.jpg',
    'media/sv_5.jpg',
]

news_titles = [
    'Конференция НАКС',
    'Общее собрание',
    'Семинар НАКС',
    'Вебинар НАКС',
]

documents = [
    'media/document1.doc',
    'media/document2.doc',
    'media/document3.doc',
    'media/document4.doc'
]

center_photos = [
    'media/center_1.jpg',
    'media/center_2.jpg',
    'media/center_3.jpg',
    'media/center_4.jpg',
    'media/center_5.jpg',
    'media/center_6.jpg',
]

menu_urls = [
    'ABOUT_US', 'ASSP', 'ASSV', 'ATTSP', 'ATTST', 'COK', 'CONTACT', 'DOKZAYAV',
    'INFO', 'OBLD', 'OBLDATT', 'PROFST', 'REGISTRY', 'RKNK', 'SPECSVAR', 'VSENOVOSTI', 'ZAYAV', 'SOSTAV_KOMISS'
]

menu_urls_titles = [
    'О центре', 'Аттестация сварщиков и специалистов', 'Аттестация сварщиков',
    'Аттестация специалистов', 'Аттестация сварочных технологий', 'Центр оценки квалификации',
    'Контакты', 'Документы и заявки', 'Информация для заявителей', 'Область деятельности',
    'Область аттестации', 'Профессиональные стандарты', 'Реестры', 'Разрушающий и неразрушающий контроль',
    'Спецподготовка сварщиков', 'Все новости', 'Заявки', 'Состав комиссии',
]

document_categories = [
    'Аттестация персонала',
    'Аттестация сварочных материалов',
    'Аттестация сварочного оборудования',
    'Аттестация сварочных технологий'
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        #delete all Posts, Articles, Menus and other
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Menu.objects.all().delete()
        Post.objects.all().delete()
        Article.objects.all().delete()
        PostPhoto.objects.all().delete()
        DocumentCategory.objects.all().delete()
        Document.objects.all().delete()
        Contact.objects.all().delete()
        Profile.objects.all().delete()
        Service.objects.all().delete()
        Attestat.objects.all().delete()
        Chunk.objects.all().delete()
        CenterPhotos.objects.all().delete()


        #upload_center_photos
        for i in range(0, len(center_photos)):
            mixer.blend(
                CenterPhotos,
                image=File(open(center_photos[i], 'rb')),
                number=i+1
            )

        #make Chunk for page "About"
        mixer.blend(
            Chunk,
            title='Описание для страницы "о центре"',
            code='about_center',
            html="""
                <p><span style="font-size:18px">Центр аттестации ВВР-2ГАЦ</span></p>
                <p><span style="font-size:18px">Организация является членом Саморегулируемая организация Ассоциация &laquo;НАКС&raquo;.</span></p>
                <p><span style="font-size:18px">Общество с ограниченной ответственностью Аттестационный центр &laquo;НАКС-Владимир&raquo; - является членом СРО Ассоциация&nbsp;&laquo;Национальное Агентство Контроля Сварки&raquo; Системы Аттестации Сварочного производства (САСв) Ростехнадзора и оказывает услуги по аттестации сварщиков и специалистов сварочного производства.</span></p>
                <p><span style="font-size:18px">Директор Герасимова Татьяна Васильевна</span></p>
                <p><span style="font-size:18px">Заместитель директора Лопанов Илья Юрьевич</span></p>
                <p><span style="font-size:18px">Исполнительный директор Сазонов Сергей Феликсович</span></p>
            """
            )

        #make Attestats
        print('Загружаем демо-аттестаты...')
        for i in range(0, len(attestats)):
            mixer.blend(
                Attestat,
                image=File(open(attestats[i], 'rb'))
            )
            print(' Загружен демо-аттестат {}'.format(i+1))

        #make PostPhotos
        print('Загружаем картинки...')
        for i in range(0, len(images)):
            #make Tags
            mixer.blend(Tag),
            #make Categories
            # mixer.blend(Category),
            #make Posts without pictures
            mixer.blend(
                Post,
                title=random.choice(news_titles),
                publish_on_main_page=True,
                publish_on_news_page=True,
                published_date=timezone.now(),
                )
            mixer.blend(PostPhoto,
                        image=File(open(images[i], 'rb')))
            #make Articles
            mixer.blend(Article),
            mixer.blend(Contact)
            print('Загружена демо-картинка {}'.format(i+1))
            print('Создана демо-статья {}'.format(i+1))



        #make Menus
        for i in range(0, len(menu_urls)):
            mixer.blend(Menu, url_code=menu_urls[i], url=reverse(
                'details', kwargs={'pk': Post.objects.first().pk}),
                title=menu_urls_titles[i])

        for i in range(0, len(document_categories)):
            mixer.blend(DocumentCategory, name=document_categories[i])
            mixer.blend(Service, title=document_categories[i], html="""
                        <hr>
                        <p>Страница в разработке</p>
                        <hr>
                """)

        print('Загружаем демо-документы...')
        for i in range(0, len(documents)):
            mixer.blend(
                Document,
                document=File(open(documents[i], 'rb')),
                category=DocumentCategory.objects.get(
                    pk=random.choice(
                        [category.pk for category in DocumentCategory.objects.all()]
                        ))
            )
            print('Заружен демо-документ {}'.format(i+1))

        print('Создаем демо-профиль...')
        mixer.blend(
            Profile,
            org_full_name='Общество с ограниченной ответственностью "Сварка трубопроводов',
            org_short_name='ООО "Сварка трубопроводов"',
            org_phones='+7 (3842)44-14-90, +7(3842)44-14-92',
            org_email='svarka@naks.ru',
            org_header_email='svarka@naks.ru',
            org_intro="""
                Центр осуществляет аттестационную деятельность в рамках Системы аттестации сварочного производства
                Ростехнадзора (САСв Ростехнадзора), независимую оценку квалификации в области сварки,
                а также оказывает услуги специальной подготовки сварщиков, и специалистов сварочного производства.
                проводит аттестацию сварочного производства (в т.ч. персонала, оборудования, материалов и технологий сварки).
            """,
            org_history="""
                Наша организация аккредитована в области аттестации сварочного производства САСв с января 2000 года. Центр осуществляет
                аттестацию персонала на выполнение сварочных работ (I уровень - сварщик), руководство и технический контроль
                за проведением сварочных работ, включая работы по технической подготовке производства и разработку
                производственно-технологической и нормативной документации (II –IV уровень - специалисты), преподавателей и
                экзаменаторов для всех групп опасных технических устройств. Центр аккредитован для всех видов аттестации
                сварочного оборудования, сварочных материалов и сварочных технологий.
            """,
            org_main_phone="+7(925)601-14-00",
            org_main_phone_text="Многоканальный",
            org_secondary_phone="+7(925)601-14-00",
            org_secondary_phone_text="Бухгалтерия",
            org_header_emails="""svarka@naks.ru, <br>
                                svarka1@naks.ru""",
            org_header_phones='+7 (3842)44-14-90 <br>+7(3842)44-14-92',
            org_address='109469, г. Владимир, улица Полины Осипенко, дом 66',
            org_address_map_link="https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3Af0AYyonWlZv3y9KCrhIOKmz2nH5lreSu&amp;width=607&amp;height=529&amp;lang=ru_RU&amp;scroll=true",
            org_csp_code='ВВР-1ЦСП',
            org_csp_reestr_link="http://naks.ru",
            org_acsp_code='ВВР-2ГАЦ',
            org_acsp_reestr_link="http://naks.ru",
            org_acsm_code='АЦСМ-12',
            org_acsm_reestr_link="http://naks.ru",
            org_acso_code='АЦСО-55',
            org_acso_reestr_link="http://naks.ru",
            org_acst_code='АЦСТ-73',
            org_acst_reestr_link="http://naks.ru",
            org_cok_code='ЦОК-37',
            org_cok_reestr_link='http://naks.ru',
        )
        print('Демо-профиль {} создан'.format(Profile.objects.first().org_short_name))


        # Category.objects.create(name=settings.ACSP_CODE)
        # Category.objects.create(name=settings.CSP_CODE)
        # Category.objects.create(name=settings.ACSO_CODE)
        # Category.objects.create(name=settings.ACST_CODE)
        # for i in range(0, len(images)):
        #     PostPhoto.objects.create(
        #         title ='image{}'.format(i),
        #         image=File(open(images[i], 'rb')))
        print('*********fill_db_complete (демо-данные созданы)************')