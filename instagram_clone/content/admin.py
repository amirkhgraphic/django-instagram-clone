from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from content.models import Post, PostMedia, PostMention, Story, StoryMention
from user_activity.models import PostLike, Comment, StoryLike
from utils.admin.mixins import LinkifyMixin, DateListFilterMixin, ActionsMixin, ThumbnailMixin, InlineMixin


class CommentInline(InlineMixin, admin.StackedInline):
    model = Comment


class PostMediaInline(InlineMixin, admin.StackedInline):
    fields = ('render_media', 'media', 'type', 'is_active', 'created_at')
    readonly_fields = ('render_media', 'created_at')
    model = PostMedia

    def render_media(self, obj):
        if obj.type == 'IMAGE':
            return format_html(
                f'<img src="{obj.media.url}" style="max-height:250px;" />'
            )
        elif obj.type == 'VIDEO':
            return format_html(
                f'<video style="max-height:250px;" controls><source src="{obj.media.url}" type="video/mp4"></video>'
            )
        else:
            return "Unsupported"

    render_media.short_description = 'Media'


class PostMentionInline(InlineMixin, admin.StackedInline):
    model = PostMention


class PostLikeInline(InlineMixin, admin.TabularInline):
    model = PostLike


class StoryMentionInline(InlineMixin, admin.StackedInline):
    model = StoryMention


class StoryLikeInline(InlineMixin, admin.TabularInline):
    model = StoryLike


@admin.register(Post)
class PostAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    list_display = ('id', 'user_link', 'likes_count', 'close_friends_only', 'likes_count_display', 'comment_is_allowed', 'created_at', 'updated_at', 'is_active')
    list_filter = ('user', 'close_friends_only', 'likes_count_display', 'comment_is_allowed') + DateListFilterMixin.list_filter
    fields = ('caption', 'user', 'likes_count', 'close_friends_only', 'likes_count_display', 'comment_is_allowed', 'created_at', 'updated_at', 'is_active')
    inlines = (PostMentionInline, PostLikeInline, CommentInline, PostMediaInline)
    readonly_fields = ('likes_count', 'created_at', 'updated_at')
    search_fields = ('caption', )
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_likes=Count('post_likes'))
        return queryset

    def likes_count(self, obj):
        return obj.num_likes

    likes_count.short_description = 'Likes'


@admin.register(Story)
class StoryAdmin(LinkifyMixin, DateListFilterMixin, ActionsMixin, ThumbnailMixin, admin.ModelAdmin):
    list_display = ('id', 'user_link', 'likes_count', 'close_friends_only', 'likes_count_display', 'created_at', 'updated_at', 'is_active')
    list_filter = ('user', 'close_friends_only', 'likes_count_display') + DateListFilterMixin.list_filter
    fields = ('render_media', 'media', 'media_type', 'caption', 'user', 'likes_count', 'close_friends_only', 'likes_count_display', 'created_at', 'updated_at', 'is_active')
    inlines = (StoryMentionInline, StoryLikeInline)
    readonly_fields = ('render_media', 'likes_count', 'created_at', 'updated_at')
    search_fields = ('caption', )
    ordering = ('-created_at', '-updated_at')

    actions = ('activate_objects', 'deactivate_objects')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_likes=Count('story_likes'))
        return queryset

    def likes_count(self, obj):
        return obj.num_likes

    likes_count.short_description = 'Likes'

    def render_media(self, obj):
        if obj.media_type == 'IMAGE':
            return format_html(
                f'<img src="{obj.media.url}" style="max-height:250px;" />'
            )
        elif obj.media_type == 'VIDEO':
            return format_html(
                f'<video style="max-height:250px;" controls><source src="{obj.media.url}" type="video/mp4"></video>'
            )
        else:
            return "Unsupported"

    render_media.short_description = 'Render Media'
