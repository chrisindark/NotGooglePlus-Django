import binascii
import logging
import os
from random import choice

from apps.articles.models import Article
from apps.posts.models import Post
from apps.profiles.models import Profile

logger = logging.getLogger(__name__)


# utility function to create random posts for random users
def posts_seeder():
    for i in range(100):
        title = binascii.hexlify(os.urandom(20)).decode()
        content = title * 4
        users = Profile.objects.all()
        u_count = users.count()
        logger.debug(f"User count: {u_count}")
        user = choice(users)
        post = Post.objects.create(title=title, content=content, user=user)
        logger.debug(f"Post created successfully: {post.pk}")
        pass


# utility function to create random articles for random users
def articles_seeder():
    for i in range(100):
        title = binascii.hexlify(os.urandom(20)).decode()
        description = title * 2
        content = title * 8
        users = Profile.objects.all()
        u_count = users.count()
        logger.debug(f"User count: {u_count}")
        user = choice(users)
        article = Article.objects.create(
            title=title, description=description, content=content, user=user
        )
        logger.debug(f"Article created successfully: {article.pk}")
        pass
