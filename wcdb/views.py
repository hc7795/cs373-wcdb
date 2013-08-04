from django.http import HttpResponse
from django.template import RequestContext, loader

from wcdb.models import Crisis, Organization, Person

#search
import re
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

#search

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
	
	
#search
def normalize_query(query_string,
					findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
					normspace=re.compile(r'\s{2,}').sub):
	''' Splits the query string in invidual keywords, getting rid of unecessary spaces
		and grouping quoted words together.
		Example:
		
		>>> normalize_query('  some random  words "with   quotes  " and   spaces')
		['some', 'random', 'words', 'with quotes', 'and', 'spaces']
	
	'''
	return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
	''' Returns a query, that is a combination of Q objects. That combination
		aims to search keywords within a model by testing the given search fields.
	
	'''
	query = None # Query to search for every search term        
	terms = normalize_query(query_string)
	for term in terms:
		or_query = None # Query to search for a given term in each field
		for field_name in search_fields:
			q = Q(**{"%s__icontains" % field_name: term})
			if or_query is None:
				or_query = q
			else:
				or_query = or_query | q
		if query is None:
			query = or_query
		else:
			query = query & or_query
	return query

def search(request):
	

	query_string = ''
	found_ppl = []
	found_crisis = []
	found_org = []
	# ppl_model = ["name", "location", "kind", "crises", "organizations"]

	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

	if query_string != '':
		entry_ppl = get_query(query_string, ['name', 'id', 'location', 'kind', 'crises', 'organizations'])
		found_ppl = Person.objects.filter(entry_ppl)

		# for field in ppl_model:
		# 	entry_ppl = get_query(query_string,[field])
		# 	filter_ppl = Person.objects.filter(entry_ppl)
		# 	if filter_ppl.exists():
		# 		context = filter_ppl.values(field)
		# 	found_ppl += [filter_ppl,context]

		# for ppl in Person.objects.all():
		# 	for field in ppl_model:
				# entry_ppl = get_query(query_string,[field])
				# filter_ppl = Person.objects.get(entry_ppl)


		entry_crisis = get_query(query_string, ['id', 'name', 'kind', 'location', 'organizations', 'date', 'time', 'humanImpact', 'economicImpact', 'resourcesNeeded', 'waytoHelp', 'people'])
		found_crisis = Crisis.objects.filter(entry_crisis)
		entry_org = get_query(query_string, ['name', 'id', 'location', 'kind', 'crises', 'history', 'contact', 'people'])
		found_org = Organization.objects.filter(entry_org)


	return render_to_response('search.html',
						  { 'query_string': query_string, 'found_ppl': found_ppl, 'found_crisis': found_crisis, 'found_org': found_org },
						  context_instance=RequestContext(request))
