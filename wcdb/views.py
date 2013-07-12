# Create your views here.

from django.http import HttpResponse
from wcdb.models import Crisis 

def CrisesAll(request):
  crises = Crisis.objects.all().order_by('crisisName')
  context = { 'crises': crises }
  #return render_to_response("crisesAll.html", context, context_instance-RequestContext(request))
"""
def PeopleAll(request):
	people = Person.objects.all().order_by('name')
	context = { 'people' : people }

def OrganizationsAll(request):
	organizations = Organization.objects.all().order_by('name')
	context = { 'organizations' = organizations } 
"""
