from contact.models import Comment, MailToAdmin, Post

from django.contrib import admin


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['image', 'header', 'short_description', 'description', 'is_active']}),
    ]
    list_display = ['header', 'short_description', 'description', 'is_active']
    search_fields = ['header']
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['post', 'username', 'text', 'is_published']}),
    ]
    list_display = ['post', 'username', 'text', 'is_published']
    list_filter = ['username', 'post', 'is_published']
    search_fields = ['username']


class MailToAdminAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'from_mail', 'text']}),
    ]
    list_display = ['username', 'from_mail', 'text', 'date']
    list_filter = ['username']
    search_fields = ['username']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MailToAdmin, MailToAdminAdmin)
