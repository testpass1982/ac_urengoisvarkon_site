from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
from django.http import HttpRequest
from mainapp.models import Post, Document, DocumentCategory, SidePanel
from mainapp.models import Service, CenterPhotos, Profstandard, Contact, Profile
# from http import HTTPStatus
from django.shortcuts import get_object_or_404
from mixer.backend.django import mixer
import random
from django.core.files import File
from django.contrib.auth.models import User


# Create your tests here.

# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1+1, 3)

class SiteTest(TestCase):
    # def setUp(self):
    def test_main_page_loads_without_errors(self):
        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Главная страница</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'mainapp/index.html')

    def test_can_create_and_publish_posts(self):
        for i in range(3):
            mixer.blend(Post, publish_on_main_page=True)
        response = self.client.get(reverse('index'))
        self.assertTrue(len(response.context['basement_news']), 3)
        post_details_response = self.client.get(
            reverse('details_news', kwargs={'pk': Post.objects.first().pk})
            )
        html = post_details_response.content.decode('utf8')
        self.assertTemplateUsed(post_details_response, 'mainapp/details_news.html')
        self.assertTrue(post_details_response.status_code, 200)
        self.assertIn(Post.objects.first().title, html)
        self.assertIn(Post.objects.first().text, html)

    def test_can_open_posts_by_details_url(self):
        posts = mixer.cycle(3).blend(Post, publish_on_main_page=True)
        for post in posts:
            url = reverse('details_news', kwargs={'pk': post.pk})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(response.context['post'], Post))
            self.assertEqual(post.title, response.context['post'].title)
            self.assertTrue('related_posts' in response.context)
            self.assertTrue(post not in response.context['related_posts'])

    def test_can_create_link_holders_and_open_pages(self):
        side_panel = mixer.blend(SidePanel)
        post_center_info = mixer.blend(Post, url_code='CENTER_INFO', title="About us", side_panel=mixer.SELECT)
        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        self.assertTrue('About us' in html)
        details_response = self.client.get(reverse('details', kwargs={'pk': post_center_info.pk}))
        self.assertTrue(details_response.status_code, 200)
        details_html = details_response.content.decode('utf8')
        self.assertTrue(post_center_info.title in details_html)
        self.assertTemplateUsed(details_response, 'mainapp/page_details.html')
        self.assertTrue('side_panel' in details_response.context)
        self.assertTrue(side_panel.text in details_html)

    def test_can_create_documents_and_publish_them_with_categories(self):
        docs = ['media/document1.doc', 'media/document2.doc', 'media/document3.doc']
        document_categories = mixer.cycle(3).blend(DocumentCategory)
        documents = mixer.cycle(10).blend(
            Document,
            document=File(open(random.choice(docs), 'rb')),
            category=mixer.SELECT
            )
        response = self.client.get(reverse('doc'))
        self.assertTemplateUsed(response, 'mainapp/doc.html')
        self.assertTrue(Document.objects.first() in response.context['docs'])
        self.assertTrue(DocumentCategory.objects.first() in response.context['categories'])
        html = response.content.decode('utf8')
        for doc in Document.objects.all():
            # self.assertTrue(doc.title in html)
            self.assertTrue(doc.category.name in html)
            self.assertTrue(doc.title in html)

    def test_can_open_all_site_pages(self):
        self.assertTrue(self.client.get(reverse('index')).status_code, 200)
        self.assertTrue(self.client.get(reverse('doc')).status_code, 200)
        mixer.blend(Post)
        self.assertTrue(self.client.get(reverse('details', kwargs={'pk': Post.objects.first().pk})).status_code, 200)
        mixer.blend(Service)
        self.assertTrue(self.client.get(reverse('service_details', kwargs={'pk': Service.objects.first().pk})).status_code, 200)
        self.assertTrue(self.client.get(reverse('cok')).status_code, 200)
        self.assertTrue(self.client.get(reverse('profstandarti')).status_code, 200)
        self.assertTrue(self.client.get(reverse('contacts')).status_code, 200)

    def test_can_upload_photos_and_publish_them(self):
        photos = ['media/center_1.jpg', 'media/center_2.jpg', 'media/center_3.jpg']
        for photo in photos:
            mixer.blend(CenterPhotos, image=File(open(photo, 'rb')))

        response = self.client.get(reverse('index'))
        html = response.content.decode('utf8')
        for photo in CenterPhotos.objects.all():
            self.assertTrue(photo.image.url in html)

    def test_can_make_profstandards_and_publish_them(self):
        profstandards = mixer.cycle(6).blend(Profstandard)
        response = self.client.get(reverse('profstandarti'))
        html = response.content.decode('utf8')
        self.assertTemplateUsed(response, 'mainapp/profstandarti.html')
        self.assertTrue(Profstandard.objects.first() in response.context['profstandards'])
        for ps in profstandards:
            self.assertTrue(ps.title in html)
            self.assertTrue(ps.document.url in html)

    def test_can_make_contacts_and_publish_them(self):
        contacts = mixer.cycle(5).blend(Contact)
        response = self.client.get(reverse('contacts'))
        self.assertTrue('contacts' in response.context)
        for contact in contacts:
            self.assertTrue(contact.title in response.content.decode('utf8'))
            self.assertTrue(contact.description in response.content.decode('utf8'))
            self.assertTrue(contact.phone in response.content.decode('utf8'))
            self.assertTrue(contact.email in response.content.decode('utf8'))

    def test_can_load_profile_import_file(self):
        user = mixer.blend(User)
        response = self.client.get('/admin/')
        self.client.force_login(user)
        import_file = File(open('media/import_file_example.txt', 'r'))
        # post a file
        self.client.post('/import_profile/', {'file': import_file})
        # check if posted file updates org profile
        with open('media/import_file_example.txt', 'r') as file:
            for line in file.readlines():
                arr = line.split('::')
                if arr[0] == 'org_short_name':
                    self.assertEqual(arr[1].strip(), Profile.objects.first().org_short_name)
                if arr[0] == 'org_main_phone':
                    self.assertEqual(arr[1].strip(), Profile.objects.first().org_main_phone)
        self.assertTrue(Profile.objects.first() is not None)
        # now logout
        self.client.logout()
        # check if admin panel not present on page
        self.assertNotIn(
            '<div class="admin_panel row bg-light p-3">',
            self.client.get('/').content.decode('utf8')
            )
        # self.assertRedirects('/import_profile/')
