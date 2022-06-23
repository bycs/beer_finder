from beers.models.bars import Bar, BarBranch
from beers.models.beers import Beer

from django.contrib import admin


class BarAdmin(admin.ModelAdmin):
    model = Bar
    list_display = ("name", "website")


class BarBranchAdmin(admin.ModelAdmin):
    model = BarBranch
    list_display = ("bar", "metro")


class BeerAdmin(admin.ModelAdmin):
    model = Beer
    list_display = ("name", "price_rub", "bar")
    list_filter = ("bar__name",)
    ordering = ("name",)
    search_fields = ("name", "bar__name")


admin.site.register(Bar, BarAdmin)
admin.site.register(BarBranch, BarBranchAdmin)
admin.site.register(Beer, BeerAdmin)
