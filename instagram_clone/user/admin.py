from django.contrib import admin
from django.utils.html import format_html

from content.admin import PostMediaInline, PostMentionInline, PostLikeInline, CommentInline
from content.models import Post
from user.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from user_profile.models import Profile
from utils.admin.mixins import DateListFilterMixin


class ProfileInline(admin.StackedInline):
    fields = ('render_image', 'image', 'bio', 'is_private', 'is_active', 'created_at', 'updated_at',)
    readonly_fields = ('render_image', 'created_at', 'updated_at')
    model = Profile

    def render_image(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" width="50px" style="max-height:50px;" />'
        )

    render_image.short_description = 'Profile Image'


# class PostInline(admin.StackedInline):
#     model = Post


@admin.register(User)
class MyUserAdmin(UserAdmin, DateListFilterMixin):
    list_display = ('email', 'user_name', 'first_name', 'last_name', 'created_at', 'last_login', 'is_active', 'is_staff')
    list_filter = ('first_name', 'last_name')
    inlines = (ProfileInline, )
    readonly_fields = ('created_at', 'last_login')
    search_fields = ('email', 'user_name', 'first_name', 'last_name')
    ordering = ('-created_at',)
    fieldsets = (
        (_('basic'), {'fields': ('email', 'user_name', 'first_name', 'last_name')}),
        (_('Personal'), {'fields': ('about',)}),
        (_('Important dates'), {'fields': ('created_at', 'last_login')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        ('Required Fields', {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1', 'password2'),
        }),
        ('Optional Fields', {
            'classes': ('wide',),
            'fields': ('about', 'is_active', 'is_staff'),
        }),
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)
