# Register your models here.

from django.contrib import admin

from .models import Userinfo, Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('body', {'fields': ['body']}),
    ]

    class CommentInline(admin.TabularInline):
        model = Comment
        extra = 1

    inlines = [CommentInline]


class UserinfoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'phone_number']}),
    ]

    class ArticleInline(admin.TabularInline):
        model = Article
        extra = 1

    inlines = [ArticleInline]


admin.site.register(Userinfo, UserinfoAdmin)
admin.site.register(Article, ArticleAdmin)
