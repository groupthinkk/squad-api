from django.contrib import admin

from .models import User, Post, Normalization
from .tasks import update_all_posts
from .forms import UserAdminForm


class UserAdmin(admin.ModelAdmin):

    form = UserAdminForm
    actions = ['update_user_posts']
    list_display = ['id', 'username', 'user_id']

    def update_user_posts(self, request, queryset):
        tasks = []
        for user in queryset:
            tasks.append(update_all_posts.delay(user))
        n = len([t for t in tasks if t])
        self.message_user(
            request,
            '{0} task{1} successfully spawned.'.format(n, '' if n == 1 else 's'),
        )

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'user', 'caption', 'created_datetime']
    list_filter = ['user']

admin.site.register(Post, PostAdmin)
admin.site.register(Normalization)
