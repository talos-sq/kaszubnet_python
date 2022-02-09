from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from kaszubnet_app.models import *

admin.site.site_header = "Panel administracyjny KaszubNet'a"
admin.site.site_title = "Panel administracyjny KaszubNet'a"


@admin.register(Ability)
class AbilityAdmin(admin.ModelAdmin):
    model = Ability

    list_display = ('name', 'level', 'description')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    model = Character

    list_display = ('name', 'rank', 'function', 'outpost')


@admin.register(OTs)
class OTsAdmin(admin.ModelAdmin):
    model = OTs


@admin.register(WarehouseItems)
class OTsAdmin(admin.ModelAdmin):
    model = WarehouseItems


@admin.register(WarehouseLog)
class OTsAdmin(admin.ModelAdmin):
    model = WarehouseLog