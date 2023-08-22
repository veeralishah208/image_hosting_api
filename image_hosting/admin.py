from django.contrib import admin
from .models import ImageStorage, Plan, Thumbnail, Subscription
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ThumbnailInline(admin.TabularInline):
    model = Thumbnail

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'plan_name',
        'original_link'
    ]
    list_editable = ('original_link',)
    list_per_page = 30
    inlines = [
        ThumbnailInline,
    ]

admin.site.register(ImageStorage)


class SubscriptionInline(admin.TabularInline):
    model = Subscription

admin.site.unregister(User)
class UserAdminSite(UserAdmin):

    inlines = [
        SubscriptionInline,
    ]

admin.site.register(User, UserAdminSite)
