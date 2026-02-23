from django.contrib import admin

from bugs.models import Bug


# Register your models here.

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    ...