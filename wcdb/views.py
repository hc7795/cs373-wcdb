from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from wcdb.models import Crisis, Organization, Person

#search
import re
import ast
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
	imagesList = crisis.common.images.all()
	location = replaceBrackets(crisis.location)
	humanImpact = replaceBrackets(crisis.humanImpact)
	economicImpact = replaceBrackets(crisis.economicImpact)
	ppl = replaceBrackets(crisis.people)
	org = replaceBrackets(crisis.organizations)
	externalLinks = crisis.common.externalLinks.all()

	strToList = ppl.split(",", 10)
	associatedPeople = []
	for person in strToList:		
		try:
			found = Person.objects.get(id=(person.encode('utf-8')).strip())
			name = unicode(found.name)
			foundID = unicode(found.slug)
			associatedPeople.append((name,foundID))
		except ObjectDoesNotExist as e:
			pass

	strToList = org.split(",", 10)
	associatedOrganizations = []
	for org in strToList:		
		try:
			found = Organization.objects.get(id=(org.encode('utf-8')).strip())
			name = unicode(found.name)
			foundID = unicode(found.slug)
			associatedOrganizations.append((name,foundID))
		except ObjectDoesNotExist as e:
			pass

	# d is a dictionary of data to be passed to the view.
	d = {}
	d["crisis"] = crisis

	# Add optional elements to d.
	if associatedPeople:
		d["associatedPeople"] = associatedPeople
	if associatedOrganizations:
		d["associatedOrganizations"] = associatedOrganizations
	if imagesList:
		d["imagesList"] = imagesList
	if location:
		d["location"] = location
	if humanImpact:
		d["humanImpact"] = humanImpact
	if economicImpact:
		d["economicImpact"] = economicImpact
	if externalLinks:
		d["externalLinks"] = externalLinks

	template = loader.get_template("crisis.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))



def person(request, urlSlug):

	person = Person.objects.get(slug=urlSlug)
	imagesList = person.common.images.all()
	crises = replaceBrackets(person.crises)
	org = replaceBrackets(person.organizations)
	externalLinks = person.common.externalLinks.all()

	strToList = crises.split(",", 10)
	associatedCrises = []
	for crisis in strToList:	
		try:	
			found = Crisis.objects.get(id=(crisis.encode('utf-8')).strip())
			name = unicode(found.name)
			foundID = unicode(found.slug)
			associatedCrises.append((name,foundID))
		except ObjectDoesNotExist as e:
			pass


	orgInfo = ""
	associatedOrganizations = []
	if org != "":
		strToList = org.split(",", 10)
		for org in strToList:	
			try:	
				found = Organization.objects.get(id=(org.encode('utf-8')).strip())
				name = unicode(found.name)
				foundID = unicode(found.slug)
				associatedOrganizations.append((name,foundID))
			except ObjectDoesNotExist as e:
				pass

	# d is a dictionary of data to be passed to the view.
	d = {}
	d["person"] = person

	# Add optional elements to d.
	if associatedCrises:
		d["associatedCrises"] = associatedCrises
	if associatedOrganizations:
		d["associatedOrganizations"] = associatedOrganizations
	if imagesList:
		d["imagesList"] = imagesList
	if externalLinks:
		d["externalLinks"] = externalLinks

	template = loader.get_template("person.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))




def org(request, urlSlug):

	org = Organization.objects.get(slug=urlSlug)
	imagesList = org.common.images.all()
	history = replaceBrackets(org.history)
	contact = replaceBrackets(org.contact)
	crises = replaceBrackets(org.crises)
	ppl = replaceBrackets(org.people)
	externalLinks = org.common.externalLinks.all()

	strToList = crises.split(",", 10)
	associatedCrises = []
	for crisis in strToList:		
		try:
			found = Crisis.objects.get(id=(crisis.encode('ascii')).strip())
			name = unicode(found.name)
			foundID = unicode(found.slug)
			associatedCrises.append((name,foundID))
		except ObjectDoesNotExist as e:
			pass

	associatedPeople = ""
	associatedPeople = []
	if ppl != "":
		strToList = ppl.split(",", 10)
		for person in strToList:	
			try:	
				found = Person.objects.get(id=(person.encode('ascii')).strip())
				name = unicode(found.name)
				foundID = unicode(found.slug)
				associatedPeople.append((name,foundID))
			except ObjectDoesNotExist as e:
				pass

	# d is a dictionary of data to be passed to the view.
	d = {}
	d["org"] = org

	# Add optional elements to d.
	if associatedCrises:
		d["associatedCrises"] = associatedCrises
	if associatedPeople:
		d["associatedPeople"] = associatedPeople
	if imagesList:
		d["imagesList"] = imagesList
	if history:
		d["history"] = history
	if contact:
		d["contact"] = contact
	if externalLinks:
		d["externalLinks"] = externalLinks


	template = loader.get_template("organization.html")
	context = RequestContext(request, d)
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
	
	crisisFields = [field.name for field in Crisis._meta.fields]
	peopleFields = [field.name for field in Person._meta.fields]
	orgFields =    [field.name for field in Organization._meta.fields]

	# Fields to remove from search.
	crisisFields.remove("id")
	crisisFields.remove("common")
	crisisFields.remove("slug")
	peopleFields.remove("id")
	peopleFields.remove("common")
	peopleFields.remove("slug")
	orgFields.remove("id")
	orgFields.remove("common")
	orgFields.remove("slug")

	queryString = ''
	queryStringBackup = ''

	# These contain dictionaries with {k, v} pairs of {object, list of matching attributes}.
	# Each list of matching attributes is a 2 tuple of (nameOfMatchingAttributeAsString, matchingAttributeContents)
	foundPeople = {}
	foundCrises = {}
	foundOrgs = {}

	searched = False

	# Retrieve query string if given.
	if ('q' in request.GET):
		searched = True
		if request.GET['q'].strip():
			queryStringBackup = request.GET['q']
			queryString = queryStringBackup.lower().strip()

	# Find and bundle up all matches.
	if queryString != '':

		queryResults = get_query(queryString, crisisFields)
		matchingCrises = Crisis.objects.filter(queryResults)

		for crisis in matchingCrises:
			foundCrises[crisis] = [];

			if queryString in crisis.name.lower():
				foundCrises[crisis] += [("name", crisis.name)]

			if queryString in crisis.kind.lower():
				foundCrises[crisis] += [("kind", crisis.kind)]

			locationList = ''
			crisisLocation = ast.literal_eval(crisis.location)
			for eachLocation in crisisLocation:
				if queryString in eachLocation.lower():
					if locationList != '':
						locationList += '; ' + eachLocation
					else:
						locationList += eachLocation
			foundCrises[crisis] += [("location", locationList)]

			humanImpactList = ''
			crisisHumanImpact = ast.literal_eval(crisis.humanImpact)
			for eachHumanImpact in crisisHumanImpact:
				if queryString in eachHumanImpact.lower():
					if humanImpactList != '':
						humanImpactList += '; ' + eachHumanImpact
					else:
						humanImpactList += eachHumanImpact
			foundCrises[crisis] += [("human impact", humanImpactList)]

			economicImpactList = ''
			crisisEconomicImpact = ast.literal_eval(crisis.economicImpact)
			for eachEconomicImpact in crisisEconomicImpact:
				if queryString in eachEconomicImpact.lower():
					if economicImpactList != '':
						economicImpactList += '\n'  '' + eachEconomicImpact
					else:
						economicImpactList += eachEconomicImpact
			foundCrises[crisis] += [("economic impact", economicImpactList)]

			if queryString in crisis.resourcesNeeded.lower():
				foundCrises[crisis] += [("resources needed", crisis.resourcesNeeded)]

			if queryString in crisis.waytoHelp.lower():
				foundCrises[crisis] += [("ways to help", crisis.waytoHelp)]

			if queryString in crisis.people.lower():
				foundCrises[crisis] += [("associated people", crisis.people)]

			if queryString in crisis.organizations.lower():
				foundCrises[crisis] += [("associated organizations", crisis.organizations)]


		queryResults = get_query(queryString, peopleFields)
		matchingPeople = Person.objects.filter(queryResults)
		
		for person in matchingPeople:
			foundPeople[person] = [];

			if queryString in person.name.lower():
				foundPeople[person] += [("name", person.name)]

			if queryString in person.kind.lower():
				foundPeople[person] += [("occupation", person.kind)]

			if queryString in person.location.lower():
				foundPeople[person] += [("location", person.location)]

			if queryString in person.crises.lower():
				foundPeople[person] += [("associated crises", person.crises)]

			if queryString in person.organizations.lower():
				foundPeople[person] += [("associated organizations", person.organizations)]


		queryResults = get_query(queryString, orgFields)
		matchingOrgs = Organization.objects.filter(queryResults)
		
		for org in matchingOrgs:
			foundOrgs[org] = [];

			if queryString in org.name.lower():
				foundOrgs[org] += [("name", org.name)]

			if queryString in org.kind.lower():
				foundOrgs[org] += [("kind", org.kind)]

			if queryString in org.location.lower():
				foundOrgs[org] += [("location", org.location)]

			if queryString in org.history.lower():
				foundOrgs[org] += [("history", org.history)]

			if queryString in org.contact.lower():
				foundOrgs[org] += [("contact info", org.contact)]

			if queryString in org.crises.lower():
				foundOrgs[org] += [("associated crises", org.crises)]

			if queryString in org.people.lower():
				foundOrgs[org] += [("associated people", org.people)]

	

	valuesToPass = {'searched': searched, 'query': queryStringBackup, 'foundPeople': foundPeople, 'foundCrises': foundCrises, 'foundOrgs': foundOrgs }
	valuesToPass["numberOfResults"] = len(foundCrises)+len(foundPeople)+len(foundOrgs)

	return render_to_response('search.html', valuesToPass, context_instance=RequestContext(request))
