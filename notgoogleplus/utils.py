# utility function to create random posts for random users
def posts_seeder():
    import os
    import binascii
    from random import choice
    for i in range(100):
        title = binascii.hexlify(os.urandom(20)).decode()
        content = title * 4
        users = Profile.objects.all()
        u_count = users.count()
        user = choice(users)
        post = Post.objects.create(
            title=title,
            content=content,
            user=user
        )
        pass

# utility function to create random articles for random users
def articles_seeder():
    import os
    import binascii
    from random import choice
    for i in range(100):
        title = binascii.hexlify(os.urandom(20)).decode()
        description = title * 2
        content = title * 8
        users = Profile.objects.all()
        u_count = users.count()
        user = choice(users)
        article = Article.objects.create(
            title=title,
            description=description,
            content=content,
            user=user
        )
        pass
