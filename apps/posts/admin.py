from django.contrib import admin

from .models import Post, PostComment, FileUpload, PostLike

# Register your models here.
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(FileUpload)
admin.site.register(PostLike)
