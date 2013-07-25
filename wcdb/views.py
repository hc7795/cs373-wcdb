from django.http import HttpResponse
from django.template import RequestContext, loader

from wcdb.models import Crisis, Organization, Person



def index(request):
	# Uncomment below when we want to move on from hardcoded pages.
	crises = Crisis.objects.all().order_by('name')
	organizations = Organization.objects.all().order_by('name')
	peeps = Person.objects.all().order_by('name')

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
	crises = Crisis.objects.all().order_by('name')
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
		"name" : "Crises",
		"type" : "crisis"
	})
	return HttpResponse(template.render(context))



def people(request):
	peeps = Person.objects.all().order_by('name')
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
		"name" : "Peeps",
		"type" : "person"
	})
	return HttpResponse(template.render(context))



def organizations(request):
	orgs = Organization.objects.all().order_by('name')
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
		"name" : "Organizations",
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
		pplInfo.append(person)
		
		# found = Crisis.objects.get(id=person)
		# name = found.name
		# foundID = found.id
		# pplInfo.append((name,foundID))




	template = loader.get_template("crisis.html")
	context = RequestContext(request, {
		"crisis" : crisis,
		"list" : l,
		"location": location,
		"humanImpact": humanImpact,
		"economicImpact": economicImpact,
		"people": ppl,
		"organizations": org,
		"externalLinks" : externalLinks,
		"stuff": strToList
	})
	return HttpResponse(template.render(context))



def person(request, urlSlug):

	person = Person.objects.get(slug=urlSlug)
	l = person.common.images.all()[0]
	crises = replaceBrackets(person.crises)
	org = replaceBrackets(person.organizations)
	externalLinks = person.common.externalLinks.all()[0]

	crises = Crisis.objects.get(id=crises)
	org = Organization.objects.get(id=org)

	template = loader.get_template("person.html")
	context = RequestContext(request, {
		"person" : person,
		"list" : l,
		"crises" : crises,
		"organizations": org,
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

	d = {
		"org" : org,
		"list" : l,
		"history": history,
		"contact": contact,
		"externalLinks" : externalLinks,
		 # "crises" : crises
	}

	strToList = crises.split(',')
	# crises = Crisis.objects.get(id=crises)
	crisisList =[]
	for a in strToList:
		crisisList.append(Crisis.objects.get(id=str(a).strip('u')))
	d["crises"] = strToList

	if ppl.strip() != "":
		ppl = Person.objects.get(id=ppl)
		d["people"] = ppl



	template = loader.get_template("organization.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))

def replaceBrackets(stringToReplace):
	stringAnswer = (stringToReplace).replace('[','')
	stringAnswer = (stringAnswer).replace(']','')
	stringAnswer = (stringAnswer).replace("'","")
	return stringAnswer