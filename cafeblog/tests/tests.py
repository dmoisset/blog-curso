from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


def clear_db():
    User.objects.all().delete()


class CafeBlogViewsTest(TestCase):
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
        response = self.client.post(url, post_data)

        url = reverse('cafeblog:index')
        self.assertRedirects(response, url)
        self.assertEqual(User.objects.all().count(), 1)

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
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), 0)

    def test_post_error_password_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {'username': u'usuario_test',
                     'email': u'usuario_test@gmail.com',
                     'password': u'123456',
                     'password2': u'abcdef',
                     }
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), 0)

    def test_post_error_email_sign_up_view(self):
        url = reverse('cafeblog:signup')
        post_data = {'username': u'usuario_test',
                     'email': u'usuario_testQgmail.com',
                     'password': u'123456',
                     'password2': u'123456',
                     }
        self.client.post(url, post_data)
        self.assertEqual(User.objects.all().count(), 0)

    def tearDown(self):
        clear_db()
