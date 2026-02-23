from django.contrib import admin

from battles.models import Battle


# Register your models here.

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    ...