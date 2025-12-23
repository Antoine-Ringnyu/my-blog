# from xml.etree.ElementTree import Comment
from django.contrib import admin

# Register your models here.

from .models import Like, User, Category, Tag, Post, Comment
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # fields = ['username', 'email', 'first_name', 'last_name', 'date_joined', ('is_staff', 'is_active',)]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
            (None, {
                'fields': ('author', 'title', 'content', 'featured_image',  'status')
            }),
            ('Category & Tags', {
                'fields': ('category', 'tags',)
            }),
            ('Verify post', {
                'fields': ('verified',)
            }),
        )
    list_display = ('title', 'author', 'status','verified','category', 'created_at')
    list_filter = ('status', 'created_at', 'category')
    search_fields = ('title', 'content')
    
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'status', 'created_at')

