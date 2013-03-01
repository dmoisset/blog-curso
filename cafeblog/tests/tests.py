from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from model_factories import UserFactory, BlogFactory
from django.core.exceptions import ObjectDoesNotExist
from django.test.client import RequestFactory
from cafeblog.views import edit_article, NO_UNIQUE_TITLE_ERROR
from cafeblog.models import Article
from django.utils import timezone
from mock import patch
import datetime


def clear_db():
    User.objects.all().delete()


TEST_PASSWORD = 'testpass'


class CafeBlogViewsTest(TestCase):
    username_default = "default"
    password_default = "password"

    def setUp(self):
        "Initial Setup"
        user_default, created = User.objects.get_or_create(username=self.username_default)
        user_default.set_password(self.password_default)
        user_default.save()

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

        url = reverse('cafeblog:login')
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


class NewBlogViewTest(TestCase):
    def setUp(self):
        """
        Create a logged in user
        """
        self.logged_user = UserFactory(password=TEST_PASSWORD)
        self.client.login(username=self.logged_user.username,
                          password=TEST_PASSWORD)

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


class NewArticleViewTest(TestCase):
    def setUp(self):
        """
        Create a logged in user, an author and a blog
        """
        self.logged_user = UserFactory(password=TEST_PASSWORD)
        self.client.login(username=self.logged_user.username,
                          password=TEST_PASSWORD)
        self.author = UserFactory(password=TEST_PASSWORD)
        self.blog = BlogFactory(administrator=self.logged_user)
        self.blog.authors.add(self.author)

        self.stranger = UserFactory(password=TEST_PASSWORD)

    def tearDown(self):
        clear_db()

    def _blog_url(self):
        """
        Returns the blog's url where the new article is going to be created
        """
        return reverse('cafeblog:new_article',
                       kwargs={'blog_pk': self.blog.pk})

    def _art_data(self):
        """
        Returns some post data to create an article against this view
        """
        return {'title': 'Test article', 'contents': 'Test content'}

    def test_get_new_article_view(self):
        """
        Expect 200 status code for a logged in user
        """
        response = self.client.get(self._blog_url())
        self.assertEquals(response.status_code, 200)

    def test_new_article_template_used(self):
        url = self._blog_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cafeblog/article_form.html')

    def test_get_new_article_view_login_required(self):
        """
        Login is required when creating a new article
        """
        self.client.logout()  # Ensure we are logged out
        url = self._blog_url()
        redirect_url = '{0}?next={1}'.format(reverse('cafeblog:login'), url)
        response = self.client.get(url)
        self.assertRedirects(response, redirect_url)

    def test_post_new_article_view_login_required(self):
        """
        Login is required when creating a new article
        """
        self.client.logout()  # Ensure we are logged out
        url = self._blog_url()
        redirect_url = '{0}?next={1}'.format(reverse('cafeblog:login'), url)
        response = self.client.post(url)
        self.assertRedirects(response, redirect_url)

    def test_blog_exists(self):
        pass

    def test_admin_can_create_article(self):
        """
        The admin of a blog can create articles for it.
        """
        url = self._blog_url()
        self.client.post(url, self._art_data())
        article = self.logged_user.article_set.get(title='Test article',
                                                   contents='Test content')
        self.assertEquals(article.author.pk, self.logged_user.pk)

    def test_author_can_create_article(self):
        """
        The author of a blog can create articles for it.
        """
        # Login the author
        self.client.login(username=self.author.username, password=TEST_PASSWORD)
        url = self._blog_url()
        self.client.post(url, self._art_data())
        article = self.author.article_set.get(title='Test article',
                                                   contents='Test content')
        self.assertEquals(article.author.pk, self.author.pk)

    def test_create_new_article_with_unauthorized_user(self):
        """
        An unauthorized_user shoud get a 403 status code
        """
        # Login an stranger
        self.client.login(username=self.stranger.username, password=TEST_PASSWORD)

        url = self._blog_url()
        resp = self.client.post(url, self._art_data())
        self.assertEquals(resp.status_code, 403)

    def test_non_author_cannot_create_article(self):
        """
        Only blog authors create articles for it.
        """
        # Login an stranger
        self.client.login(username=self.stranger.username, password=TEST_PASSWORD)

        url = self._blog_url()
        self.client.post(url, self._art_data())

        with self.assertRaises(ObjectDoesNotExist):
           self.stranger.article_set.get(title='Test article')

    def test_article_belongs_to_blog(self):
        """
        An article should be created on the given blog only
        """
        url = self._blog_url()
        self.client.post(url, self._art_data())

        art = self.blog.article_set.get(title='Test article')
        self.assertEquals(art.blog.pk, self.blog.pk)

    def test_article_title_is_unique(self):
        """
        An article should have a unique title within a blog
        """
        art_data = self._art_data()
        art_data.update({
            'author': self.logged_user,
            'pub_date': timezone.now(),
            'creation_time': timezone.now(),
            'last_modified': timezone.now()
        })
        art = Article(**art_data)
        self.blog.article_set.add(art)

        # Now try creating an article with the same title again
        url = self._blog_url()
        resp = self.client.post(url, self._art_data())
        self.assertFormError(resp, 'article_form', 'title', NO_UNIQUE_TITLE_ERROR)

    def test_article_publication_date(self):
        """
        A newly created article shoud have the creation time set to now
        """
        now = datetime.datetime(2013, 12, 1, 12, 30, 50, 0, tzinfo=timezone.get_default_timezone())

        url = self._blog_url()
        with patch.object(timezone, 'now', return_value=now):
            req = RequestFactory().post(url, self._art_data())
            req.user = self.logged_user
            edit_article(req, self.blog.pk)
        art = self.logged_user.article_set.get(title='Test article')
        self.assertEquals(art.creation_time, now)
