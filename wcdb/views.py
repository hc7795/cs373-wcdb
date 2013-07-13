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
	template = loader.get_template('CRI_IRAQWR.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def CRI_HURIKE(request):
	template = loader.get_template("CRI_HURIKE.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def CRI_BAGAIR(request):
	template = loader.get_template("CRI_BAGAIR.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def ORG_WHLORG(request):
	template = loader.get_template("ORG_WHLORG.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def ORG_REDCRS(request):
	template = loader.get_template("ORG_REDCRS.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def ORG_IAVETA(request):
	template = loader.get_template("ORG_IAVETA.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def PER_SADHUS(request):
	template = loader.get_template("PER_SADHUS.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def PER_BUSDAD(request):
	template = loader.get_template("PER_BUSDAD.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))

def PER_BRAMAN(request):
	template = loader.get_template("PER_BRAMAN.html")
	context = RequestContext(request)
	return HttpResponse(template.render(context))
