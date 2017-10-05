from django.test import TestCase

from notgoogleplus.apps.profiles.models import Profile
from .models import Post, PostComment


# Create your tests here.
class TestPostModel(TestCase):
    def setup(self):
        self.post = Post(title='title', content='content', user=Profile.objects.get(user__username='christopherp'))
        self.save()

    def test_post_creation(self):
        try:
            Post.objects.get(title='title', content='content', user=Profile.objects.get(user__username='christopherp')) is not None
        except AssertionError:
            raise AssertionError

    def test_post_representation(self):
        self.assertEqual(self.post.title, str(self.post)

    def test_post_deletion(self):
        self.post.delete()


class TestPostApi(ApiTestCase):
    def setup(self):
        self.post = Post(title='title', content='content', user=User.objects.get(username='christopherp'))
        self.save()
    pass
