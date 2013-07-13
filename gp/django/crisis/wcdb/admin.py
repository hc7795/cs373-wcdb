
from django.contrib import admin
from wcdb.models import Person, Organization, Crisis 

#admin.site.register(Crisis, CrisisAdmin)
admin.site.register(Person)
admin.site.register(Organization)
admin.site.register(Crisis)

