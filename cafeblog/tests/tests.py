from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from model_factories import UserFactory, BlogFactory


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


class NewBlogViewTest(TestCase):
    def setUp(self):
        """
        Create a logged in user
        """
        self.logged_user = UserFactory(password='testpass')
        self.client.login(username=self.logged_user.username,
                          password='testpass')

    def test_get_new_blog_view(self):
        """
        Expect 200 status code for a logged in user
        """
        url = reverse('cafeblog:new_blog')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_blog_template_used(self):
        url = reverse('cafeblog:new_blog')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cafeblog/blog_form.html')

    def test_get_new_blog_view_login_required(self):
        """
        Login required when creating a new blog
        """
        self.client.logout()  # Ensure we are logged out
        url = reverse('cafeblog:new_blog')
        redirect_url = '{0}?next={1}'.format(reverse('cafeblog:login'), url)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)

    def test_post_new_blog_view_login_required(self):
        """
        Login required when creating a new blog
        """
        self.client.logout()  # Ensure we are logged out
        url = reverse('cafeblog:new_blog')
        redirect_url = '{0}?next={1}'.format(reverse('cafeblog:login'), url)
        response = self.client.post(url)
        self.assertRedirects(response, redirect_url)

    def test_post_new_blog(self):
        """
        Creating a new blog should assing the current user as admin and author
        """
        url = reverse('cafeblog:new_blog')
        self.client.post(url, {'title': 'Test blog',
                                        'description': 'Test description'})
        blog = self.logged_user.blog_set.get(title='Test blog',
                                             description='Test description')
        self.assertEquals(blog.administrator.pk, self.logged_user.pk)
        self.assertEquals(blog.authors.get(pk=self.logged_user.pk).pk, self.logged_user.pk)

    def tearDown(self):
        clear_db()
