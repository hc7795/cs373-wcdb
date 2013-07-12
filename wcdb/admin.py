from django.contrib import admin
from wcdb.models import Person, Organization, Crisis 

#admin.site.register(Crisis, CrisisAdmin)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Crisis)

"""
class CrisisAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name', 'org', 'people')
	search_fields = ['name']
"""
