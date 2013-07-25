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
	print "slug: " + str(urlSlug)

	template = loader.get_template("crisis.html")
	context = RequestContext(request, {
		"crisis" : crisis
	})
	return HttpResponse(template.render(context))



def person(request, urlSlug):

	person = Person.objects.get(slug=urlSlug)
	print "slug: " + str(urlSlug)

	template = loader.get_template("person.html")
	context = RequestContext(request, {
		"person" : person
	})
	return HttpResponse(template.render(context))



def org(request, urlSlug):

	org = Organization.objects.get(slug=urlSlug)
	print "slug: " + str(urlSlug)

	template = loader.get_template("organization.html")
	context = RequestContext(request, {
		"org" : org
	})
	return HttpResponse(template.render(context))