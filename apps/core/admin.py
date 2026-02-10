from django.contrib import admin
from .models import Banner, ContactSubmission, StaticPage, Notification

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('section',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    search_fields = ('user__mobile_number', 'title')

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}