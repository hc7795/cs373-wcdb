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
	# Uncomment below when we want to move on from hardcoded pages.
	# crises = Crisis.objects.all().order_by('CrisisName')
	# organizations = Organization.objects.all().order_by('OrganizationName')
	# people = Person.objects.all().order_by('PersonName')

	crises = []
	crises.append(Crisis.objects.get(CrisisID="CRI_IRAQWR"))
	crises.append(Crisis.objects.get(CrisisID="CRI_HURIKE"))
	crises.append(Crisis.objects.get(CrisisID="CRI_BAGAIR"))

	organizations = []
	organizations.append(Organization.objects.get(OrganizationID="ORG_WHLORG"))
	organizations.append(Organization.objects.get(OrganizationID="ORG_REDCRS"))
	organizations.append(Organization.objects.get(OrganizationID="ORG_IAVETA"))

	people = []
	people.append(Person.objects.get(PersonID="PER_SADHUS"))
	people.append(Person.objects.get(PersonID="PER_BUSDAD"))
	people.append(Person.objects.get(PersonID="PER_BRAMAN"))

	template = loader.get_template("splash.html")
	context = RequestContext(request, {
		"crises" : crises,
		"organizations" : organizations,
		"people" : people
	})

	return HttpResponse(template.render(context))

def CRI_IRAQWR(request):
	return HttpResponse("CRI_IRAQWR")

def CRI_HURIKE(request):
	return HttpResponse("CRI_HURIKE")

def CRI_BAGAIR(request):
	return HttpResponse("CRI_BAGAIR")

def ORG_WHLORG(request):
	return HttpResponse("ORG_WHLORG")

def ORG_REDCRS(request):
	return HttpResponse("ORG_REDCRS")

def ORG_IAVETA(request):
	return HttpResponse("ORG_IAVETA")

def PER_SADHUS(request):
	return HttpResponse("PER_SADHUS")

def PER_BUSDAD(request):
	return HttpResponse("PER_BUSDAD")

def PER_BRAMAN(request):
	return HttpResponse("PER_BRAMAN")
