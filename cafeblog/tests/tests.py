from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User


def clear_db():
    User.objects.all().delete()


class CafeBlogViewsTest(TestCase):
    username_default = "default"
    password_default = "password"

    def setUp(self):
        "Initial Setup"
        user_default, created = User.objects.get_or_create(username=self.username_default)
        user_default.set_password(self.password_default)
        user_default.save()

        self.client = Client()

    def test_get_index_view(self):
        url = reverse('cafeblog:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeblog/index.html')

    def test_post_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {'username': u'usuario_test',
                     'email': u'usuario_test@gmail.com',
                     'password': u'123456',
                     'password2': u'123456',
                     }
        users_count = User.objects.all().count()
        response = self.client.post(url, post_data)

        url = reverse('cafeblog:index')
        self.assertRedirects(response, url)
        self.assertEqual(User.objects.all().count(), users_count + 1)

        user = User.objects.all().order_by('-pk')[0]
        self.assertEqual(user.username, u'usuario_test')
        self.assertEqual(user.email, u'usuario_test@gmail.com')

    def test_post_error_username_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {
                     'email': u'usuario_test@gmail.com',
                     'password': u'123456',
                     'password2': u'123456',
                     }
        users_count = User.objects.all().count()
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), users_count)

    def test_post_error_password_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {'username': u'usuario_test',
                     'email': u'usuario_test@gmail.com',
                     'password': u'123456',
                     'password2': u'abcdef',
                     }
        users_count = User.objects.all().count()
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), users_count)

    def test_post_error_email_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {'username': u'usuario_test',
                     'email': u'usuario_testQgmail.com',
                     'password': u'123456',
                     'password2': u'123456',
                     }
        users_count = User.objects.all().count()
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), users_count)

    ######################################
    # Testing views when user is logged in
    ######################################

    def test_get_blogs_list_view(self):
        self.client.login(username=self.username_default, password=self.password_default)

        url = reverse('cafeblog:blogs_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeblog/blogs_list.html')
        self.assertContains(response, 'Were not found blogs.')


     ######################################
    # Testing views when user is not logged in
    ######################################

    def test_get_not_logged_blogs_list_view(self):
        url = reverse('cafeblog:blogs_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        clear_db()
