from beers.models import Bar, BarBranch, Beer

from django.contrib import admin


class BarAdmin(admin.ModelAdmin):
    list_display = ("name", "website")


class BarBranchAdmin(admin.ModelAdmin):
    list_display = ("bar", "metro")


class BeerAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "bar")


admin.site.register(Bar, BarAdmin)
admin.site.register(BarBranch, BarBranchAdmin)
admin.site.register(Beer, BeerAdmin)
