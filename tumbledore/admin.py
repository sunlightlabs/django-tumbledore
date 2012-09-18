from django.contrib import admin

from tumbledore.models import *


class TumblelogPostInline(admin.StackedInline):
    model = TumblelogPost
    list_editable = ('is_published', 'is_sticky')
    prepopulated_fields = {"slug": ("title",), }


class TumblelogWidgetPlacementInline(admin.TabularInline):
    model = TumblelogWidgetPlacement


class TumblelogAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'mount_on', 'theme', 'is_active', 'sort_posts_by', 'created_at')
    list_filter = ('theme', 'is_active')
    list_editable = ('theme', 'is_active', 'sort_posts_by')
    date_hierarchy = 'created_at'
    inlines = (TumblelogWidgetPlacementInline, TumblelogPostInline)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('name', 'mount_on', 'theme', 'posts_per_page')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description', 'sort_posts_by', 'extra_styles', 'extra_scripts')
        }),
    )
admin.site.register(Tumblelog, TumblelogAdmin)


class TumblelogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tumblelog', 'is_published', 'is_sticky', 'created_at', 'published_at')
    list_filter = ('author', 'tumblelog', 'is_published', 'is_sticky')
    list_editable = ('is_published', 'is_sticky')
    date_hierarchy = 'published_at'
    prepopulated_fields = {"slug": ("title",), }
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'tumblelog', 'author', 'content',
                       'is_published', 'is_sticky', 'has_permalink', 'published_at')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('excerpt', 'sort_order', 'custom_data')
        }),
    )
admin.site.register(TumblelogPost, TumblelogPostAdmin)


class TumblelogWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    date_hierarchy = 'created_at'
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
admin.site.register(TumblelogWidget, TumblelogWidgetAdmin)


class TumblelogWidgetPlacementAdmin(admin.ModelAdmin):
    list_display = ('widget', 'tumblelog', 'order')
    list_editable = ('order',)
admin.site.register(TumblelogWidgetPlacement, TumblelogWidgetPlacementAdmin)
