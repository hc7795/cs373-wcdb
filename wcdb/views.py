from django.http import HttpResponse
from django.template import RequestContext, loader

from wcdb.models import Crisis, Organization, Person

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

def index(request):
	crises = Crisis.objects.all().order_by('CrisisName')
	organizations = Organization.objects.all().order_by('OrganizationName')
	people = Person.objects.all().order_by('PersonName')

	template = loader.get_template("splash.html")
	context = RequestContext(request, {
		"crises" : crises,
		"organizations" : organizations,
		"people" : people
	})

	return HttpResponse(template.render(context))
