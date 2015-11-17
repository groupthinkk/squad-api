from django.conf.urls import url
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.template.response import TemplateResponse

from .models import (
    User, Post, PostComparison, PostComparisonQueue, PostComparisonQueueMember,
    Follow,
)
from .tasks import (
    update_user, update_user_posts, add_user, update_user_follows,
)
from .forms import UserAdminForm


def _task_message(n):
    return '{0} task{1} successfully spawned.'.format(n, '' if n == 1 else 's')


class UserAdmin(admin.ModelAdmin):

    form = UserAdminForm
    actions = [
        'update_user_data',
        'update_user_posts',
        'update_user_follows',
    ]
    list_display = [
        'image_tag',
        'name',
        'username',
        'user_id',
        'followers',
        'friends_and_family',
        'ff_follows',
    ]
    list_filter = ['friends_and_family']

    def get_queryset(self, request):
        return User.objects.annotate(ff_follows=Count('follows_user'))

    def ff_follows(self, obj):
        return obj.ff_follows
    ff_follows.short_description = 'Friends & Family follows'
    ff_follows.admin_order_field = 'ff_follows'

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        my_urls = [
            url(r'^bulk_add/$', self.admin_site.admin_view(self.bulk_add)),
        ]
        return my_urls + urls

    def bulk_add(self, request):
        context = dict(
            self.admin_site.each_context(request),
        )

        if request.method == 'POST':
            usernames = request.POST['usernames'].strip().replace(',', ' ').split()
            friends_and_family = request.POST.get('friends_and_family', False)

            for username in usernames:
                add_user.delay({
                    'username': username,
                    'friends_and_family': friends_and_family,
                })

        return TemplateResponse(request, 'admin/bulk_add.html', context)

    def update_user_data(self, request, queryset):
        tasks = []
        for user in queryset:
            tasks.append(update_user.delay(user))
        ntasks = len([t for t in tasks if t])
        self.message_user(request, _task_message(ntasks))

    def update_user_posts(self, request, queryset):
        tasks = []
        for user in queryset:
            tasks.append(update_user_posts.delay(user))
        ntasks = len([t for t in tasks if t])
        self.message_user(request, _task_message(ntasks))

    def update_user_follows(self, request, queryset):
        tasks = []
        for user in queryset:
            tasks.append(update_user_follows.apply_async(
                args=[user],
                queue='crawler',
            ))
        ntasks = len([t for t in tasks if t])
        self.message_user(request, _task_message(ntasks))

admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):

    list_display = ['image_tag', 'user', 'caption', 'created_datetime']
    list_filter = ['user']
    ordering = ['-created_datetime']
    actions = [
        'create_comparison',
    ]

    def create_comparison(self, request, queryset):
        if queryset.count() != 2:
            self.message_user(
                request,
                'Exactly two posts must be selected to create a comparison.',
                level=messages.ERROR,
            )
            return

        post_a, post_b = list(queryset)
        comparison = PostComparison(post_a=post_a, post_b=post_b)

        try:
            comparison.clean()
        except ValidationError as ve:
            self.message_user(request, '\n'.join(ve), level=messages.ERROR)
            return

        try:
            comparison.save()
        except IntegrityError:
            self.message_user(
                request,
                'Comparison already exists!',
                level=messages.ERROR,
            )
            return

        self.message_user(
            request,
            'Comparison created!',
            level=messages.SUCCESS,
        )


admin.site.register(Post, PostAdmin)


class PostComparisonAdmin(admin.ModelAdmin):

    list_display = ['user', 'post_a_summary', 'post_b_summary']
    list_filter = ['user']

    def has_add_permission(self, request):
        return False

admin.site.register(PostComparison, PostComparisonAdmin)


class PostComparisonQueueMemberInline(admin.TabularInline):

    model = PostComparisonQueueMember
    readonly_fields = ['queue', 'comparison']
    extra = 1


class PostComparisonQueueAdmin(admin.ModelAdmin):

    list_display = ['id', 'name']
    inlines = [PostComparisonQueueMemberInline]
    exclude = ['comparisons']

admin.site.register(PostComparisonQueue, PostComparisonQueueAdmin)


class PostComparisonQueueMemberAdmin(admin.ModelAdmin):

    list_display = ['id', 'queue_id', 'comparison_id']

admin.site.register(PostComparisonQueueMember, PostComparisonQueueMemberAdmin)


class FollowAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'follows_user']

admin.site.register(Follow, FollowAdmin)
