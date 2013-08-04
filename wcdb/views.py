from django.http import HttpResponse
from django.template import RequestContext, loader

from wcdb.models import Crisis, Organization, Person



def index(request):
	# Uncomment below when we want to move on from hardcoded pages.
	crises = Crisis.objects.all().order_by('?')
	organizations = Organization.objects.all().order_by('?')
	peeps = Person.objects.all().order_by('?')

	crisesToPass = []
	orgsToPass = []
	peepsToPass = []

	for crisis in crises:
		try:
			l = crisis.common.images.all()[0]
			crisesToPass.append((crisis, l))
		except:
			pass

	for org in organizations:
		try:
			l = org.common.images.all()[0]
			orgsToPass.append((org, l))
		except:
			pass

	for peep in peeps:
		try:
			l = peep.common.images.all()[0]
			peepsToPass.append((peep, l))
		except:
			pass

	template = loader.get_template("index.html")
	context = RequestContext(request, {
		"crises" : crisesToPass,
		"organizations" : orgsToPass,
		"people" : peepsToPass
	})
	return HttpResponse(template.render(context))



def crises(request):
	crises = Crisis.objects.all().order_by('?')
	crisesToPass = []
	for crisis in crises:
		try:
			l = crisis.common.images.all()[0]
			crisesToPass.append((crisis, l))
		except:
			pass

	template = loader.get_template("gallery.html")
	context = RequestContext(request, {
		"modelObjects" : crisesToPass,
		"name" : "crises",
		"type" : "crisis"
	})
	return HttpResponse(template.render(context))



def people(request):
	peeps = Person.objects.all().order_by('?')
	peepsToPass = []
	for peep in peeps:
		try:
			l = peep.common.images.all()[0]
			peepsToPass.append((peep, l))
		except:
			pass

	template = loader.get_template("gallery.html")
	context = RequestContext(request, {
		"modelObjects" : peepsToPass,
		"name" : "people",
		"type" : "person"
	})
	return HttpResponse(template.render(context))



def organizations(request):
	orgs = Organization.objects.all().order_by('?')
	orgsToPass = []
	for org in orgs:
		try:
			l = org.common.images.all()[0]
			orgsToPass.append((org, l))
		except:
			pass
	template = loader.get_template("gallery.html")
	context = RequestContext(request, {
		"modelObjects" : orgsToPass,
		"name" : "organizations",
		"type" : "org"
	})
	return HttpResponse(template.render(context))



def about(request):
	template = loader.get_template("about.html")
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))



def crisis(request, urlSlug):

	crisis = Crisis.objects.get(slug=urlSlug)
	l = crisis.common.images.all()[0]
	location = replaceBrackets(crisis.location)
	humanImpact = replaceBrackets(crisis.humanImpact)
	economicImpact = replaceBrackets(crisis.economicImpact)
	ppl = replaceBrackets(crisis.people)
	org = replaceBrackets(crisis.organizations)
	externalLinks = crisis.common.externalLinks.all()[0]

	strToList = ppl.split(",",10)
	pplInfo = []
	for person in strToList:		
		found = Person.objects.get(id=(person.encode('ascii')).strip())
		name = str(found.name)
		foundID = str(found.slug)
		pplInfo.append((name,foundID))

	strToList = org.split(",",10)
	orgInfo = []
	for org in strToList:		
		found = Organization.objects.get(id=(org.encode('ascii')).strip())
		name = str(found.name)
		foundID = str(found.slug)
		orgInfo.append((name,foundID))

	template = loader.get_template("crisis.html")
	context = RequestContext(request, {
		"crisis" : crisis,
		"associatedPeople": pplInfo,
		"associatedOrganizations": orgInfo,
		"list" : l,
		"location": location,
		"humanImpact": humanImpact,
		"economicImpact": economicImpact,
		"externalLinks" : externalLinks,
	})
	return HttpResponse(template.render(context))



def person(request, urlSlug):

	person = Person.objects.get(slug=urlSlug)
	l = person.common.images.all()[0]
	crises = replaceBrackets(person.crises)
	org = replaceBrackets(person.organizations)
	externalLinks = person.common.externalLinks.all()[0]

	strToList = crises.split(",",10)
	criInfo = []
	for crisis in strToList:		
		found = Crisis.objects.get(id=(crisis.encode('ascii')).strip())
		name = str(found.name)
		foundID = str(found.slug)
		criInfo.append((name,foundID))


	orgInfo = ""
	if org != "":
		orgInfo = []
		strToList = org.split(",",10)
		for org in strToList:		
			# test.append(org.encode('ascii').strip())
			found = Organization.objects.get(id=(org.encode('ascii')).strip())
			name = str(found.name)
			foundID = str(found.slug)
			orgInfo.append((name,foundID))


	template = loader.get_template("person.html")
	context = RequestContext(request, {
		"associatedCrises" : criInfo,
		"associatedOrganizations": orgInfo,
		"person" : person,
		"list" : l,
		"externalLinks" : externalLinks
	})
	return HttpResponse(template.render(context))




def org(request, urlSlug):

	org = Organization.objects.get(slug=urlSlug)
	l = org.common.images.all()[0]
	history = replaceBrackets(org.history)
	contact = replaceBrackets(org.contact)
	crises = replaceBrackets(org.crises)
	ppl = replaceBrackets(org.people)
	externalLinks = org.common.externalLinks.all()[0]

	strToList = crises.split(",",10)
	criInfo = []
	for crisis in strToList:		
		found = Crisis.objects.get(id=(crisis.encode('ascii')).strip())
		name = str(found.name)
		foundID = str(found.slug)
		criInfo.append((name,foundID))

	pplInfo = ""
	if ppl != "":
		pplInfo =[]
		strToList = ppl.split(",",10)
		pplInfo = []
		for person in strToList:		
			found = Person.objects.get(id=(person.encode('ascii')).strip())
			name = str(found.name)
			foundID = str(found.slug)
			pplInfo.append((name,foundID))


	template = loader.get_template("organization.html")
	context = RequestContext(request, {
		"org" : org,
		"associatedCrises" : criInfo,
		"associatedPeople": pplInfo,
		"list" : l,
		"history": history,
		"contact": contact,
		"externalLinks" : externalLinks,
	})
	return HttpResponse(template.render(context))


def search(request):
	template = loader.get_template("search.html")
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))


def import_export(request):
	template = loader.get_template("import_export.html")
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))



def replaceBrackets(stringToReplace):
	stringAnswer = (stringToReplace).replace('[','')
	stringAnswer = (stringAnswer).replace(']','')
	stringAnswer = (stringAnswer).replace("'","")
	stringAnswer = (stringAnswer).replace('"','')
	return stringAnswer