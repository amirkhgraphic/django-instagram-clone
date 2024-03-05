import os

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class LinkifyMixin:
    def comment_link(self, obj):
        url = reverse("admin:blog_comment_change", args=[obj.comment.id])
        return format_html('<a href="{}">{}</a>', url, obj.comment)

    def cart_link(self, obj):
        url = reverse("admin:cart_cart_change", args=[obj.cart.id])
        return format_html('<a href="{}">{}</a>', url, obj.cart)

    def author_link(self, obj):
        url = reverse("admin:user_user_change", args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author)

    def seller_link(self, obj):
        url = reverse("admin:user_user_change", args=[obj.seller.id])
        return format_html('<a href="{}">{}</a>', url, obj.seller)

    def user_link(self, obj):
        url = reverse("admin:user_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user)

    def product_link(self, obj):
        url = reverse("admin:shop_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product)

    def post_link(self, obj):
        url = reverse("admin:blog_post_change", args=[obj.post.id])
        return format_html('<a href="{}">{}</a>', url, obj.post)

    product_link.short_description = 'Product'
    post_link.short_description = 'Post'
    author_link.short_description = 'Author'
    user_link.short_description = 'User'
    seller_link.short_description = 'Seller'
    cart_link.short_description = 'Cart'
    comment_link.short_description = 'Comment'


class DateListFilterMixin:
    list_filter = ('is_active', ('created_at', admin.DateFieldListFilter), ('updated_at', admin.DateFieldListFilter))


class ActionsMixin:
    def activate_objects(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_objects(self, request, queryset):
        queryset.update(is_active=False)

    activate_objects.short_description = "Activate selected objects"

    deactivate_objects.short_description = "Deactivate selected objects"


class ThumbnailMixin:
    def render_thumbnail(self, obj):
        return format_html(
            f'<img src="{obj.thumbnail.url}" width="50px" style="max-height:50px;" />'
        )

    render_thumbnail.short_description = 'Thumbnail'


class RenderContentMixin:
    def render_name(self, obj):
        return os.path.basename(obj.file.name).split('.')[0]

    def render_content(self, obj):
        if obj.type == 'IMAGE':
            return format_html(
                f'<img src="{obj.file.url}" width="200px" style="max-height:200px;" />'
            )
        elif obj.type == 'VIDEO':
            return format_html(
                f'<video width="200px" style="max-height:200px;" controls><source src="{obj.file.url}" '
                f'type="video/{obj.format.lower()}">Your browser does not support the video tag.</video>'
            )
        elif obj.type == 'AUDIO':
            return format_html(
                f'<audio controls><source src="{obj.file.url}" type="audio/{obj.format.lower()}">Your browser does not '
                f'support the audio element.</audio>',
            )
        else:
            return "Unsupported Format"

    def render_content_small(self, obj):
        if obj.type == 'IMAGE':
            return format_html(
                f'<img src="{obj.file.url}" width="50px" style="max-height:50px;" />'
            )
        elif obj.type == 'VIDEO':
            return format_html(
                f'<video width="50px" style="max-height:50px;" controls><source src="{obj.file.url}" '
                f'type="video/{obj.format.lower()}">Your browser does not support the video tag.</video>'
            )
        elif obj.type == 'AUDIO':
            return format_html(
                f'<audio controls><source src="{obj.file.url}" type="audio/{obj.format.lower()}">Your browser does not '
                f'support the audio element.</audio>',
            )
        else:
            return "Unsupported Format"

    render_content.short_description = 'Content'
    render_content_small.short_description = 'Content'

    render_name.short_description = 'File Name'


class InlineMixin:
    extra = 1
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)