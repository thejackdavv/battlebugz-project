from django.contrib import admin

from locations.models import Location, Food, FoodEvent


# Register your models here.

@admin.register(FoodEvent)
class FoodEventAdmin(admin.ModelAdmin):
    ...

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    ...


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    ...

