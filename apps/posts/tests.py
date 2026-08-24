from django.test import TestCase
from rest_framework.test import APITestCase

from apps.profiles import Profile
from .models import Post
from apps.users.models import User


# Create your tests here.
class TestPostModel(TestCase):
    def setup(self):
        self.post = Post(title='title',
                         content='content',
                         user=Profile.objects.get(user__username='christopherp'))
        self.save()

    def test_post_creation(self):
        try:
            Post.objects.get(title='title',
                             content='content',
                             user=Profile.objects.get(user__username='christopherp')
                             ) is not None
        except AssertionError:
            raise AssertionError

    def test_post_representation(self):
        self.assertEqual(self.post.title, str(self.post))

    def test_post_deletion(self):
        self.post.delete()


class TestPostApi(APITestCase):
    def setup(self):
        self.post = Post(title='title',
                         content='content',
                         user=User.objects.get(username='christopherp'))
        self.save()
