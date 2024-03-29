from django.contrib import admin

from beers.models.bars import Bar
from beers.models.bars import BarBranch
from beers.models.beers import Beer


class BarAdmin(admin.ModelAdmin):
    model = Bar
    list_display = ("name", "website", "updated")
    search_fields = ("name", "website")


class BarBranchAdmin(admin.ModelAdmin):
    model = BarBranch
    list_display = ("bar_branch_name", "address")
    list_filter = ("bar__name", "metro")
    search_fields = ("bar__name", "metro", "address")


class BeerAdmin(admin.ModelAdmin):
    model = Beer
    list_display = ("name", "price_rub", "bar")
    list_filter = ("bar__name",)
    ordering = ("name",)
    search_fields = ("name", "bar__name")


admin.site.register(Bar, BarAdmin)
admin.site.register(BarBranch, BarBranchAdmin)
admin.site.register(Beer, BeerAdmin)
