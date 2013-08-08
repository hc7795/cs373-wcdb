from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from wcdb.models import Crisis, Organization, Person
from random import choice

# Search.
import re
import ast
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

# File uploads.
from wcdb.models import Document
from wcdb.forms import DocumentForm
from django.core.urlresolvers import reverse


def getConciseSummary(summary):
	summaryMaxLength = 600
	if (len(summary) > summaryMaxLength):
		summary = summary[:summaryMaxLength] + "..."
	return summary


def index(request):
	objectLimit = 20

	crises = Crisis.objects.all().order_by('?')
	organizations = Organization.objects.all().order_by('?')
	peeps = Person.objects.all().order_by('?')

	crisesToPass = []
	orgsToPass = []
	peepsToPass = []

	for crisis in crises:
		try:
			l = choice(crisis.common.images.all())
			crisesToPass.append((crisis, l, getConciseSummary(crisis.common.summary)))
		except:
			pass

	for org in organizations:
		try:
			l = choice(org.common.images.all())
			orgsToPass.append((org, l, getConciseSummary(ast.literal_eval(org.history)[0])))
		except:
			pass

	for peep in peeps:
		try:
			l = choice(peep.common.images.all())
			peepsToPass.append((peep, l, getConciseSummary(peep.kind)))
		except:
			pass

	d = {}
	d["crises"] = crisesToPass[:objectLimit]
	d["organizations"] = orgsToPass[:objectLimit]
	d["people"] = peepsToPass[:objectLimit]

	template = loader.get_template("index.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))



def crises(request):
	crises = Crisis.objects.all().order_by('?')
	crisesToPass = []
	for crisis in crises:
		try:
			l = choice(crisis.common.images.all())
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
			l = choice(peep.common.images.all())
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
			l = choice(org.common.images.all())
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
	locations = ast.literal_eval(crisis.location)
	humanImpact = ast.literal_eval(crisis.humanImpact)
	economicImpact = ast.literal_eval(crisis.economicImpact)
	resourcesNeeded = ast.literal_eval(crisis.resourcesNeeded)
	waysToHelp = ast.literal_eval(crisis.waytoHelp)
	ppl = replaceBrackets(crisis.people)
	org = replaceBrackets(crisis.organizations)
	
	citations = crisis.common.citations.all()
	externalLinks = crisis.common.externalLinks.all()
	images = crisis.common.images.all()
	videos = crisis.common.videos.all()
	maps = crisis.common.maps.all()
	feeds = crisis.common.feeds.all()
	summary = crisis.common.summary

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
	topGroupSize = 0

	# Add optional elements to d.
	if associatedPeople:
		d["associatedPeople"] = associatedPeople
	if associatedOrganizations:
		d["associatedOrganizations"] = associatedOrganizations
	if resourcesNeeded and resourcesNeeded[0] != None and resourcesNeeded[0].lower() != "n/a":
		d["resourcesNeeded"] = resourcesNeeded
	if waysToHelp and waysToHelp[0] != None and waysToHelp[0].lower() != "n/a":
		d["waysToHelp"] = waysToHelp 
	if locations:
		topGroupSize += 1
		d["locations"] = locations
		d["numLocations"] = len(locations)
	if humanImpact and humanImpact[0] != None and humanImpact[0].lower() != "n/a":
		d["humanImpact"] = humanImpact
	if economicImpact and economicImpact[0] != None and economicImpact[0].lower() != "n/a":
		d["economicImpact"] = economicImpact
	if citations and citations[0] != None:
		d["citations"] = citations
	if images and images[0] != None:
		d["images"] = images
	if videos and videos[0] != None:
		d["videos"] = videos
	if maps and maps[0] != None:
		topGroupSize += 1
		d["maps"] = maps
	if feeds and feeds[0] != None:
		d["feeds"] = feeds
	if externalLinks and externalLinks[0] != None:
		d["externalLinks"] = externalLinks
	if summary:
		topGroupSize += 1
		d["summary"] = summary

	if crisis.kind != "":
		topGroupSize += 1

	if crisis.date != "" or crisis.time != "":
		topGroupSize += 1

	d["topGroupSize"] = topGroupSize

	template = loader.get_template("crisis.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))



def person(request, urlSlug):

	person = Person.objects.get(slug=urlSlug)
	location = person.location
	crises = replaceBrackets(person.crises)
	org = replaceBrackets(person.organizations)

	citations = person.common.citations.all()
	externalLinks = person.common.externalLinks.all()
	images = person.common.images.all()
	videos = person.common.videos.all()
	maps = person.common.maps.all()
	feeds = person.common.feeds.all()
	summary = person.common.summary

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
	if location and location[0] != None:
		locations = [l.strip() for l in location.split(",")]
		d["locations"] = locations
		d["numLocations"] = len(locations)
	
	if citations and citations[0] != None:
		d["citations"] = citations
	if images and images[0] != None:
		d["images"] = images
	if videos and videos[0] != None:
		d["videos"] = videos
	if maps and maps[0] != None:
		d["maps"] = maps
	if feeds and feeds[0] != None:
		d["feeds"] = feeds
	if externalLinks and externalLinks[0] != None:
		d["externalLinks"] = externalLinks
	if summary:
		d["summary"] = summary

	template = loader.get_template("person.html")
	context = RequestContext(request, d)
	return HttpResponse(template.render(context))




def org(request, urlSlug):

	org = Organization.objects.get(slug=urlSlug)
	location = org.location
	history = org.history
	contact = ast.literal_eval(org.contact)
	crises = replaceBrackets(org.crises)
	ppl = replaceBrackets(org.people)

	citations = org.common.citations.all()
	externalLinks = org.common.externalLinks.all()
	images = org.common.images.all()
	videos = org.common.videos.all()
	maps = org.common.maps.all()
	feeds = org.common.feeds.all()
	summary = org.common.summary

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
	if location and location[0] != None:
		locations = [l.strip() for l in location.split(",")]
		d["locations"] = locations
		d["numLocations"] = len(locations)
	if history and history[0] != None:
		d["history"] = ast.literal_eval(history)
	if contact and contact[0] != None:
		d["contacts"] = contact
	
	if citations and citations[0] != None:
		d["citations"] = citations
	if images and images[0] != None:
		d["images"] = images
	if videos and videos[0] != None:
		d["videos"] = videos
	if maps and maps[0] != None:
		d["maps"] = maps
	if feeds and feeds[0] != None:
		d["feeds"] = feeds
	if externalLinks and externalLinks[0] != None:
		d["externalLinks"] = externalLinks
	if summary:
		d["summary"] = summary


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

		queryResults = get_query(queryString, ["name"])

		test = ''

		queryTopplID = ''
		querypplName = Person.objects.filter(queryResults)
		for eachQuerypplName in querypplName:
			if queryTopplID != '':
				queryTopplID += ' ' + eachQuerypplName.id
			else:
				queryTopplID += eachQuerypplName.id

		test = queryTopplID


		# queryResults = get_query(queryTopplID, crisisFields)
		# matchingCrises = Crisis.objects.filter(queryResults)

		queryResults = get_query(queryString, crisisFields)
		matchingCrises = Crisis.objects.filter(queryResults)
		
		# test = matchingCrises

		foundCrises = searchInCrisis(queryString, matchingCrises, queryTopplID)

		queryResultsIDtoName = get_query(queryTopplID, crisisFields)
		matchingCrisesIDtoName = Crisis.objects.filter(queryResultsIDtoName)
		# foundCrises = searchInCrisis(queryTopplID, matchingCrisesIDtoName, queryTopplID)

		# for crisis in matchingCrises:

		# 	foundCrises[crisis] = [];

		# 	if queryString in crisis.name.lower():
		# 		foundCrises[crisis] += [("name", crisis.name)]

		# 	if queryString in crisis.kind.lower():
		# 		foundCrises[crisis] += [("kind", crisis.kind)]

		# 	locationList = ''
		# 	crisisLocation = ast.literal_eval(crisis.location)
		# 	for eachLocation in crisisLocation:
		# 		if queryString in eachLocation.lower():
		# 			if locationList != '':
		# 				locationList += '; ' + eachLocation
		# 			else:
		# 				locationList += eachLocation
		# 	if locationList != '':
		# 		foundCrises[crisis] += [("location", locationList)]

		# 	humanImpactList = ''
		# 	crisisHumanImpact = ast.literal_eval(crisis.humanImpact)
		# 	for eachHumanImpact in crisisHumanImpact:
		# 		if queryString in eachHumanImpact.lower():
		# 			if humanImpactList != '':
		# 				humanImpactList +=  '; '  + eachHumanImpact
		# 			else:
		# 				humanImpactList += eachHumanImpact
		# 	if humanImpactList != '':
		# 		foundCrises[crisis] += [("human impact", humanImpactList)]

		# 	economicImpactList = ''
		# 	crisisEconomicImpact = ast.literal_eval(crisis.economicImpact)
		# 	for eachEconomicImpact in crisisEconomicImpact:
		# 		if queryString in eachEconomicImpact.lower():
		# 			if economicImpactList != '':
		# 				economicImpactList += '; '  + eachEconomicImpact
		# 			else:
		# 				economicImpactList += eachEconomicImpact
		# 	if economicImpactList != '':
		# 		foundCrises[crisis] += [("economic impact", economicImpactList)]

		# 	resourcesNeededList = ''
		# 	crisisresourcesNeeded = ast.literal_eval(crisis.resourcesNeeded)
		# 	for eachresourcesNeeded in crisisresourcesNeeded:
		# 		if queryString in eachresourcesNeeded.lower():
		# 			if resourcesNeededList != '':
		# 				resourcesNeededList += '; ' + eachresourcesNeeded
		# 			else:
		# 				resourcesNeededList += eachresourcesNeeded
		# 	if resourcesNeededList != '':
		# 		foundCrises[crisis] += [("resources needed", resourcesNeededList)]

		# 	waytoHelpList = ''
		# 	crisiswaytoHelp = ast.literal_eval(crisis.waytoHelp)
		# 	for eachwaytoHelp in crisiswaytoHelp:
		# 		if queryString in eachwaytoHelp.lower():
		# 			if waytoHelpList != '':
		# 				waytoHelpList += '; ' + eachwaytoHelp
		# 			else:
		# 				waytoHelpList += eachwaytoHelp
		# 	if waytoHelpList != '':
		# 		foundCrises[crisis] += [("ways to help", waytoHelpList)]

			
		# 	pplList = ''
		# 	crisispeople = ast.literal_eval(crisis.people)
		# 	for eachpeople in crisispeople:
		# 		try:
		# 			pplObjects = Person.objects.get(id = eachpeople)
		# 			if queryString in pplObjects.name:
		# 				if pplList != '':
		# 					pplList += '; ' + pplObjects.name
		# 				else:
		# 					pplList += pplObjects.name
		# 		except ObjectDoesNotExist as e:
		# 			pass
		# 	if pplList != '':
		# 		foundCrises[crisis] += [("associated people", pplList)]
			

			
		# 	orgList = ''
		# 	crisisOrg = ast.literal_eval(crisis.organizations)
		# 	for eachOrg in crisisOrg:
		# 		try:
		# 			orgObjects = Organization.objects.get(id = eachOrg)
		# 			if queryString in orgObjects.name:
		# 				if orgList != '':
		# 					orgList += '; ' + orgObjects.name
		# 				else:
		# 					orgList += orgObjects.name
		# 		except ObjectDoesNotExist as e:
		# 			pass
		# 	if orgList != '':
		# 		foundCrises[crisis] += [("associated organizations", orgList)]




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

			
			crisisList = ''
			pplCrisis = ast.literal_eval(person.crises)
			for eachCrisis in pplCrisis:
				try:
					crisisObjects = Crisis.objects.get(id = eachCrisis)
					if queryString in crisisObjects.name:
						if crisisList != '':
							crisisList += '; ' + crisisObjects.name
						else:
							crisisList += crisisObjects.name
				except ObjectDoesNotExist as e:
					pass
			if crisisList != '':
				foundPeople[person] += [("associated crises", crisisList)]
			
			
			orgList = ''
			pplOrg = ast.literal_eval(person.organizations)
			for eachOrg in pplOrg:
				try:
					orgObjects = Organization.objects.get(id = eachOrg)
					if queryString in orgObjects.name:
						if orgList != '':
							orgList += '; ' + orgObjects.name
						else:
							orgList += orgObjects.name
				except ObjectDoesNotExist as e:
					pass
			if orgList != '':
				foundPeople[person] += [("associated organizations", orgList)]


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

			# history = queryListToString(queryString, ast.literal_eval(org.history))
			# if history:
			# 	foundOrgs[org] += [("history", history)]

			# contactInfo = queryListToString(queryString, ast.literal_eval(org.contact))
			# if contactInfo:
			# 	foundOrgs[org] += [("contact info", contactInfo)]

			# if queryString in org.contact.lower():
			# 	foundOrgs[org] += [("contact info", org.contact)]

			# contactList = ''
			# orgContact = ast.literal_eval(org.contact)
			# if orgContact:
			# 	for eachContact in orgContact:
			# 		if queryString in eachContact.lower():
			# 			if contactList != '':
			# 				contactList += '; ' + eachContact
			# 			else:
			# 				contactList += eachContact
			# 	if contactList != '':
			# 		foundOrgs[org] += [("contact info", contactList)]



			# if queryString in org.crises.lower():
			# 	foundOrgs[org] += [("associated crises", org.crises)]

			
			crisisList = ''
			orgCrisis = ast.literal_eval(org.crises)
			for eachCrisis in orgCrisis:
				try:
					crisisObjects = Crisis.objects.get(id = eachCrisis)
					if queryString in crisisObjects.name:
						if crisisList != '':
							crisisList += '; ' + crisisObjects.name
						else:
							crisisList += crisisObjects.name
				except ObjectDoesNotExist as e:
					pass
			if crisisList != '':
				foundOrgs[org] += [("associated crises", crisisList)]
			


			# if queryString in org.people.lower():
			# 	foundOrgs[org] += [("associated people", org.people)]

			
			pplList = ''
			orgPeople = ast.literal_eval(org.people)
			for eachpeople in orgPeople:
				try:
					pplObjects = Person.objects.get(id = eachpeople)
					if queryString in pplObjects.name:
						if pplList != '':
							pplList += '; ' + pplObjects.name
						else:
							pplList += pplObjects.name
				except ObjectDoesNotExist as e:
					pass
			if pplList != '':
				foundOrgs[org] += [("associated people", pplList)]
			
	
	test = '' 
	valuesToPass = {'searched': searched, 'query': queryStringBackup, 'foundPeople': foundPeople, 'foundCrises': foundCrises, 'foundOrgs': foundOrgs, 'test': test }
	valuesToPass["numberOfResults"] = len(foundCrises)+len(foundPeople)+len(foundOrgs)

	return render_to_response('search.html', valuesToPass, context_instance=RequestContext(request))


# Takes a list of strings and a query string. Looks for query string 
# in each string of the list, and returns a string of the found
# queries.
def queryListToString(queryString, listToQuery):
	returnString = ''
	for element in listToQuery:
		if queryString in element.lower():
			if returnString:
				returnString += '; ' + element
			else:
				returnString += element
	return returnString


def searchInCrisis(queryString, matchingCrises, queryTopplID):
	foundCrises = {}

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
		if locationList != '':
			foundCrises[crisis] += [("location", locationList)]

		humanImpactList = ''
		crisisHumanImpact = ast.literal_eval(crisis.humanImpact)
		for eachHumanImpact in crisisHumanImpact:
			if queryString in eachHumanImpact.lower():
				if humanImpactList != '':
					humanImpactList +=  '; '  + eachHumanImpact
				else:
					humanImpactList += eachHumanImpact
		if humanImpactList != '':
			foundCrises[crisis] += [("human impact", humanImpactList)]

		economicImpactList = ''
		crisisEconomicImpact = ast.literal_eval(crisis.economicImpact)
		for eachEconomicImpact in crisisEconomicImpact:
			if queryString in eachEconomicImpact.lower():
				if economicImpactList != '':
					economicImpactList += '; '  + eachEconomicImpact
				else:
					economicImpactList += eachEconomicImpact
		if economicImpactList != '':
			foundCrises[crisis] += [("economic impact", economicImpactList)]

		resourcesNeededList = ''
		crisisresourcesNeeded = ast.literal_eval(crisis.resourcesNeeded)
		for eachresourcesNeeded in crisisresourcesNeeded:
			if queryString in eachresourcesNeeded.lower():
				if resourcesNeededList != '':
					resourcesNeededList += '; ' + eachresourcesNeeded
				else:
					resourcesNeededList += eachresourcesNeeded
		if resourcesNeededList != '':
			foundCrises[crisis] += [("resources needed", resourcesNeededList)]

		waytoHelpList = ''
		crisiswaytoHelp = ast.literal_eval(crisis.waytoHelp)
		for eachwaytoHelp in crisiswaytoHelp:
			if queryString in eachwaytoHelp.lower():
				if waytoHelpList != '':
					waytoHelpList += '; ' + eachwaytoHelp
				else:
					waytoHelpList += eachwaytoHelp
		if waytoHelpList != '':
			foundCrises[crisis] += [("ways to help", waytoHelpList)]

		
		pplList = ''
		crisispeople = ast.literal_eval(crisis.people)
		for eachpeople in crisispeople:
			try:
				pplObjects = Person.objects.get(id = eachpeople)
				if (queryString in pplObjects.name) or (queryTopplID in pplObjects.id):
					if pplList != '':
						pplList += '; ' + pplObjects.name
					else:
						pplList += pplObjects.name
			except ObjectDoesNotExist as e:
				pass
		if pplList != '':
			foundCrises[crisis] += [("associated people", pplList)]
		

		
		orgList = ''
		crisisOrg = ast.literal_eval(crisis.organizations)
		for eachOrg in crisisOrg:
			try:
				orgObjects = Organization.objects.get(id = eachOrg)
				if queryString in orgObjects.name:
					if orgList != '':
						orgList += '; ' + orgObjects.name
					else:
						orgList += orgObjects.name
			except ObjectDoesNotExist as e:
				pass
		if orgList != '':
			foundCrises[crisis] += [("associated organizations", orgList)]

	return foundCrises



def fileUpload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            # return HttpResponseRedirect("import_export.html")
            # return HttpResponseRedirect(reverse('wcdb.views.fileUpload', args=[]))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'import_export.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
