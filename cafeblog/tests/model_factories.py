import factory
from cafeblog.models import Blog
from django.contrib.auth.models import User


class UserFactory(factory.Factory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    password = factory.Sequence(lambda n: 'password{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'firstname{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'lastname{0}'.format(n))
    email = factory.LazyAttribute(lambda a: '{0}.{1}@mail.com'.format(
        a.first_name, a.last_name
    ).lower())

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class BlogFactory(factory.Factory):
    FACTORY_FOR = Blog
    title = factory.Sequence(lambda n: 'Blog title {0}'.format(n))
    description = factory.Sequence(lambda n: 'Blog description {0}'.format(n))
    administrator = factory.SubFactory(UserFactory)
