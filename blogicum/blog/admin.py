from django.contrib import admin

from .models import Post, Category, Location


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'is_published',
        'title',
        'text',
        'pub_date'
    )
    ordering = ('id',)
    list_editable = ('is_published',)
    search_fields = (
        'title',
        'text'
    )
    list_filter = ('is_published',)
    list_display_links = ('title',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'id',
        'created_at',
        'is_published',
        'title',
        'description',
        'slug'
    )
    ordering = ('id',)
    list_editable = ('is_published',)
    search_fields = (
        'title',
        'description'
    )
    list_filter = ('is_published',)
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'id',
        'created_at',
        'is_published',
        'name'
    )
    ordering = ('id',)
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
