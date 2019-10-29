from django.contrib import admin
from .models import Continent, Region, Geoname, Featurecode, Countryinfo, Hierarchy

class HierarchyInline(admin.StackedInline):
    model = Hierarchy
    autocomplete_fields = ['child']
    fk_name = 'parent'

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['laender', 'geonameid']
    search_fields = ['name','laender__name']

@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    search_fields = ['name','englishname']

@admin.register(Countryinfo)
class CountryinfoAdmin(admin.ModelAdmin):
    search_fields = ['name','englishname']

@admin.register(Geoname)
class GeonameAdmin(admin.ModelAdmin):
    search_fields = ['name']
    # search decreasingly for weighted importance in an fcode and then decreasingly by population
    ordering = ['-fcode__searchorder_detail','-population']
    inlines = [ HierarchyInline ]

@admin.register(Hierarchy)
class HierarchyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['child','parent']

admin.site.register(Featurecode)

admin.site.site_header = 'RKI-Geoname Administration'



