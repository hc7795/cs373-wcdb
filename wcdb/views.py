from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

from wcdb.models import Crisis, Organization, Person
from random import choice

# URL validity checking.
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

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

from xmlParser import *


def makeValidURL(listObject):
  if listObject.href:
    if listObject.href.startswith("//"):
      listObject.href = "http:" + listObject.href

    if "embed/" in listObject.href and "youtube" in listObject.href:
      listObject.href = listObject.href[:listObject.href.find("embed/")] + "watch?v=" + listObject.href[listObject.href.find("embed/") + 6:]

  if listObject.embed:
    if listObject.embed.startswith("//"):
      listObject.embed = "http:" + listObject.embed

    if "embed/" in listObject.embed and "youtube" in listObject.embed:
      listObject.embed = listObject.embed[:listObject.embed.find("embed/")] + "watch?v=" + listObject.embed[listObject.embed.find("embed/") + 6:]

  
  return listObject

def isValidImage(listObject):
  validHref = False
  validEmbed = False

  validFileAssociations = (".png", ".jpg", ".jpeg", ".gif", ".svg")

  if listObject.href and listObject.href.endswith(validFileAssociations):
    if not "youtube" in listObject.href:
      validHref = True
  elif listObject.embed and listObject.embed.endswith(validFileAssociations):
    if not "youtube" in listObject.embed:
      validEmbed = True
  return validHref or validEmbed

def filterInvalidImages(listOfListObjects):
  return filter(isValidImage, listOfListObjects)

def isValidDataList(stringList):
  return stringList and stringList[0] != None and stringList[0].lower() != "none" and stringList[0].lower() != "n/a" and stringList[0].lower() != "not applicable" and stringList[0].lower() != "not available"

def massMakeValidURL(listOfListObjects):
  return [makeValidURL(listObject) for listObject in listOfListObjects]

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
  images = filterInvalidImages(massMakeValidURL(crisis.common.images.all()))
  videos = massMakeValidURL(crisis.common.videos.all())
  maps = massMakeValidURL(crisis.common.maps.all())
  feeds = crisis.common.feeds.all()
  summary = crisis.common.summary

  strToList = ppl.split(",", 10)
  associatedPeople = []
  for person in strToList:    
    try:
      found = Person.objects.get(id=(person.encode('utf8')).strip())
      name = unicode(found.name)
      foundID = unicode(found.slug)
      associatedPeople.append((name,foundID))
    except ObjectDoesNotExist as e:
      pass

  strToList = org.split(",", 10)
  associatedOrganizations = []
  for org in strToList:    
    try:
      found = Organization.objects.get(id=(org.encode('utf8')).strip())
      name = unicode(found.name)
      foundID = unicode(found.slug)
      associatedOrganizations.append((name,foundID))
    except ObjectDoesNotExist as e:
      pass

  # d is a dictionary of data to be passed to the view.
  d = {}
  d["crisis"] = crisis
  topGroupSize = 0
  middleGroupSize = 0

  # Add optional elements to d.
  if associatedPeople:
    d["associatedPeople"] = associatedPeople

  if associatedOrganizations:
    d["associatedOrganizations"] = associatedOrganizations

  if isValidDataList(resourcesNeeded):
    middleGroupSize += 1
    d["resourcesNeeded"] = resourcesNeeded

  if isValidDataList(waysToHelp):
    middleGroupSize += 1
    d["waysToHelp"] = waysToHelp 

  if locations:
    topGroupSize += 1
    d["locations"] = locations
    d["numLocations"] = len(locations)

  if isValidDataList(humanImpact):
    middleGroupSize += 1
    d["humanImpact"] = humanImpact

  if isValidDataList(economicImpact):
    middleGroupSize += 1
    d["economicImpact"] = economicImpact

  if citations:
    d["citations"] = citations

  if images:
    d["images"] = images

  if videos:
    d["videos"] = videos

  if maps:
    topGroupSize += 1
    d["maps"] = maps

  if feeds:
    d["feeds"] = feeds

  if externalLinks:
    d["externalLinks"] = externalLinks

  if summary:
    topGroupSize += 1
    d["summary"] = summary

  if crisis.kind != "":
    topGroupSize += 1

  if crisis.date != "" or crisis.time != "":
    topGroupSize += 1

  d["middleGroupSize"] = middleGroupSize
  d["topGroupSize"] = topGroupSize

  template = loader.get_template("crisis.html")
  context = RequestContext(request, d)
  return HttpResponse(template.render(context))



def person(request, urlSlug):

  person = Person.objects.get(slug=urlSlug)
  locations = person.location
  crises = replaceBrackets(person.crises)
  org = replaceBrackets(person.organizations)

  citations = person.common.citations.all()
  externalLinks = person.common.externalLinks.all()
  images = person.common.images.all()
  videos = massMakeValidURL(person.common.videos.all())
  maps = person.common.maps.all()
  feeds = person.common.feeds.all()
  summary = person.common.summary

  strToList = crises.split(",", 10)
  associatedCrises = []
  for crisis in strToList:  
    try:  
      found = Crisis.objects.get(id=(crisis.encode('utf8')).strip())
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
        found = Organization.objects.get(id=(org.encode('utf8')).strip())
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
  if locations:
    d["locations"] = [locations]
    d["numLocations"] = 1
  
  if citations:
    d["citations"] = citations
  if images:
    d["images"] = images
  if videos:
    d["videos"] = videos
  if maps:
    d["maps"] = maps
  if feeds:
    d["feeds"] = feeds
  if externalLinks:
    d["externalLinks"] = externalLinks
  if summary:
    d["summary"] = summary

  template = loader.get_template("person.html")
  context = RequestContext(request, d)
  return HttpResponse(template.render(context))




def org(request, urlSlug):

  org = Organization.objects.get(slug=urlSlug)
  locations = org.location
  history = ast.literal_eval(org.history)
  contact = ast.literal_eval(org.contact)
  crises = replaceBrackets(org.crises)
  ppl = replaceBrackets(org.people)

  citations = org.common.citations.all()
  externalLinks = org.common.externalLinks.all()
  images = org.common.images.all()
  videos = massMakeValidURL(org.common.videos.all())
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
  if locations:
    d["locations"] = [locations]
    d["numLocations"] = 1
  if isValidDataList(history):
    d["history"] = history
  if isValidDataList(contact):
    d["contacts"] = contact
  
  if citations:
    d["citations"] = citations
  if images:
    d["images"] = images
  if videos:
    d["videos"] = videos
  if maps:
    d["maps"] = maps
  if feeds:
    d["feeds"] = feeds
  if externalLinks:
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
  stringAnswer = (stringToReplace).replace('[', '')
  stringAnswer = (stringAnswer).replace(']', '')
  stringAnswer = (stringAnswer).replace("'", "")
  stringAnswer = (stringAnswer).replace('"', '')
  return stringAnswer
  
  
# search
def query_format(query_string,
          findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
          normspace=re.compile(r'\s{2,}').sub):

  return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def query_make(query_string, search_fields):

  query = None       
  terms = query_format(query_string)
  for term in terms:
    or_query = None
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

	test = '' #----------------------------------------------------------------------------

	# Find and bundle up all matches.
	if queryString != '':

		#check if queryString is a name of a person then get that person ID
		queryPeopleName = query_make(queryString, ["name"])
		peopleID = ''
		peopleName = Person.objects.filter(queryPeopleName)
		for eachpeopleName in peopleName:
			if peopleID != '':
				peopleID += ' ' + eachpeopleName.id
			else:
				peopleID += eachpeopleName.id

		test = peopleID

		#check if queryString is a name of an organization then get that organization ID
		queryOrgName = query_make(queryString, ["name"])
		orgID = ''
		orgName = Organization.objects.filter(queryOrgName)
		for eachorgName in orgName:
			if orgID != '':
				orgID += ' ' + eachorgName.id
			else:
				orgID += eachorgName.id

		#check if queryString is a name of a crisis then get that crisis ID
		queryCrisisName = query_make(queryString, ["name"])
		crisisID = ''
		crisisName = Crisis.objects.filter(queryOrgName)
		for eachcrisisName in crisisName:
			if crisisID != '':
				crisisID += ' ' + eachcrisisName.id
			else:
				crisisID += eachcrisisName.id


		# Crisis
		# search for queryString in CrisisObjects except people and org fields
		queryResults = query_make(queryString, crisisFields)
		matchingCrises = Crisis.objects.filter(queryResults)
		foundCrises = searchInCrisis(queryString, matchingCrises)

		# search for queryString in Crisis people field
		if peopleID:
			queryCrisisPeopleID = query_make(peopleID, crisisFields)
			matchingCrisisPeopleID = Crisis.objects.filter(queryCrisisPeopleID)
			foundCrisisPeopleName = seachPPLName(peopleID, matchingCrisisPeopleID)
			foundCrises.update(foundCrisisPeopleName)

		# search for queryString in Crisis org field
		if orgID:
			queryCrisisOrgID = query_make(orgID, crisisFields)
			matchingCrisisOrgID = Crisis.objects.filter(queryCrisisOrgID)
			foundCrisisOrgName = seachOrgName(orgID, matchingCrisisOrgID)
			foundCrises.update(foundCrisisOrgName)


		# People
		# seach for queryString in PeopleObjects except organization and crisis fields
		queryResults = query_make(queryString, peopleFields)
		matchingPeople = Person.objects.filter(queryResults)
		foundPeople = searchInPeople(queryString, matchingPeople)

		# search for queryString in People org field
		if orgID:
			queryPeopleOrgID = query_make(orgID, peopleFields)
			matchingPeopleOrgID = Person.objects.filter(queryPeopleOrgID)
			foundPeopleOrgName = seachOrgName(orgID, matchingPeopleOrgID)
			foundPeople.update(foundPeopleOrgName)

		# search for queryString in People crisis field
		if crisisID:
			queryPeopleCrisisID = query_make(crisisID, peopleFields)
			matchingPeopleCrisisID = Person.objects.filter(queryPeopleCrisisID)
			foundPeopleCrisisName = seachCrisisName(crisisID, matchingPeopleCrisisID)
			foundPeople.update(foundPeopleCrisisName)

		# Orgs
		# search for queryString in OrgObjects except people and crisis fields
		queryResults = query_make(queryString, orgFields)
		matchingOrgs = Organization.objects.filter(queryResults)
		foundOrgs = searchInOrgs(queryString, matchingOrgs)

		# search for queryString in Org people field
		if peopleID:
			queryOrgPeopleID = query_make(peopleID, orgFields)
			matchingOrgPeopleID = Organization.objects.filter(queryOrgPeopleID)
			foundOrgPeopleName = seachPPLName(peopleID, matchingOrgPeopleID)
			foundOrgs.update(foundOrgPeopleName)

		# search for queryString in Org crisis field
		if crisisID:
			queryOrgCrisisID = query_make(crisisID, orgFields)
			matchingOrgCrisisID = Organization.objects.filter(queryOrgCrisisID)
			foundOrgCrisisName = seachCrisisName(crisisID, matchingOrgCrisisID)
			foundOrgs.update(foundOrgCrisisName)
			
	valuesToPass = {'searched': searched, 'query': queryStringBackup, 'foundPeople': foundPeople, 'foundCrises': foundCrises, 'foundOrgs': foundOrgs, 'test': test }
	valuesToPass["numberOfResults"] = len(foundCrises)+len(foundPeople)+len(foundOrgs)

	return render_to_response('search.html', valuesToPass, context_instance=RequestContext(request))


def searchInCrisis(queryString, matchingCrises):
	foundCrises = {}

	for crisis in matchingCrises:

		foundCrises[crisis] = [];

		if queryString in crisis.name.lower():
			foundCrises[crisis] += [("name", crisis.name)]

		if queryString in crisis.kind.lower():
			foundCrises[crisis] += [("kind", crisis.kind)]

		# locationString = ast.literal_eval(crisis.location)
		locationList = searchContext(queryString, unicode(crisis.location))
		if locationList:
			foundCrises[crisis] += [("location", locationList)]
		# foundCrises[crisis] += [("location", locationString)]

		# if queryString in crisis.location.lower():
		# 	foundCrises[crisis] += [("location", crisis.location)]
		

		humanImpactList = searchContext(queryString, unicode(crisis.humanImpact))
		if humanImpactList:
			foundCrises[crisis] += [("human impact", humanImpactList)]

		economicImpactList = searchContext(queryString, unicode(crisis.economicImpact))
		if economicImpactList:
			foundCrises[crisis] += [("economic impact", economicImpactList)]

		resourcesNeededList = searchContext(queryString, unicode(crisis.resourcesNeeded))
		if resourcesNeededList:
			foundCrises[crisis] += [("resources needed", resourcesNeededList)]

		waytoHelpList = searchContext(queryString, unicode(crisis.waytoHelp))
		if waytoHelpList:
			foundCrises[crisis] += [("ways to help", waytoHelpList)]

		if crisis.common.summary:
			summaryList = searchContext(queryString, unicode(crisis.common.summary))
			if summaryList:
				foundCrises[crisis] += [("summary", summaryList)]

	return foundCrises

def searchInPeople(queryString, matchingPeople):
	foundPeople = {}

	for person in matchingPeople:
		foundPeople[person] = [];

		if queryString in person.name.lower():
			foundPeople[person] += [("name", person.name)]

		if queryString in person.kind.lower():
			foundPeople[person] += [("occupation", person.kind)]

		locationList = searchContext(queryString, unicode(person.location))
		if locationList:
			foundPeople[person] += [("location", locationList)]

		summaryList = searchContext(queryString, unicode(person.common.summary))
		if summaryList:
			foundPeople[person] += [("summary", summaryList)]

	return foundPeople

def searchInOrgs(queryString, matchingOrgs):
	foundOrgs = {}

	for org in matchingOrgs:
		foundOrgs[org] = [];

		if queryString in org.name.lower():
			foundOrgs[org] += [("name", org.name)]

		if queryString in org.kind.lower():
			foundOrgs[org] += [("kind", org.kind)]

		locationList = searchContext(queryString, unicode(org.location))
		if locationList:
			foundOrgs[org] += [("location", locationList)]

		historyList = searchContext(queryString, unicode(org.history))
		if historyList:
			foundOrgs[org] += [("history", historyList)]

		contactList = searchContext(queryString, unicode(org.contact))
		if contactList:
			foundOrgs[org] += [("contact info", contactList)]

		summaryList = searchContext(queryString, unicode(org.common.summary))
		if summaryList:
			foundOrgs[org] += [("summary", summaryList)]

	return foundOrgs

def seachPPLName(queryString, matchingElements):
	foundPPL = {}

	for eachElement in matchingElements:

		foundPPL[eachElement] = [];

		pplList = ''
		people = ast.literal_eval(eachElement.people)
		for eachpeople in people:
			try:
				pplObjects = Person.objects.get(id = eachpeople)
				if (queryString in pplObjects.name) or (queryString in pplObjects.id):
					if pplList != '':
						pplList += '; ' + pplObjects.name
					else:
						pplList += pplObjects.name
			except ObjectDoesNotExist as e:
				pass
		if pplList != '':
			foundPPL[eachElement] += [("associated people", pplList)]

	return foundPPL

def seachOrgName(queryString, matchingElements):
	foundOrg = {}

	for eachElement in matchingElements:

		foundOrg[eachElement] = [];

		orgList = ''
		org = ast.literal_eval(eachElement.organizations)
		for eachOrg in org:
			try:
				orgObjects = Organization.objects.get(id = eachOrg)
				if (queryString in orgObjects.name) or (queryString in orgObjects.id):
					if orgList != '':
						orgList += '; ' + orgObjects.name
					else:
						orgList += orgObjects.name
			except ObjectDoesNotExist as e:
				pass
		if orgList != '':
			foundOrg[eachElement] += [("associated organizations", orgList)]

	return foundOrg

def seachCrisisName(queryString, matchingElements):
	foundCrisis = {}

	for eachElement in matchingElements:

		foundCrisis[eachElement] = [];

		crisisList = ''
		crises = ast.literal_eval(eachElement.crises)
		for eachCrisis in crises:
			try:
				crisisObjects = Crisis.objects.get(id = eachCrisis)
				if (queryString in crisisObjects.name) or (queryString in crisisObjects.id):
					if crisisList != '':
						crisisList += '; ' + crisisObjects.name
					else:
						crisisList += crisisObjects.name
			except ObjectDoesNotExist as e:
				pass
		if crisisList != '':
			foundCrisis[eachElement] += [("associated crises", crisisList)]

	return foundCrisis

def searchContext(queryString, paragraph):

	context =''
	splitSentences = re.split('(?<!\d)[.]', paragraph)
	for eachSentence in splitSentences:
		if queryString.lower() in eachSentence.lower():
			# context += re.sub('(?i)(\s+)(%s)(\s+)'%queryString, '\\1<b>\\2</b>\\3', eachSentence) + ' ...'
		# if re.search(queryString,eachSentence, re.IGNORECASE)
			context += eachSentence 

	context = context.replace('\\n', '')
	context = context.replace('\\u', '')
	context = context.replace("u'", '')
	context = context.replace("\\'", '')
	context = replaceBrackets(context)

	return context



def fileImport(request):

	d = {}

	password = request.POST['q'].strip()
	if password != "gummypandas":
		d["success_message"] = "Bad password!"
		return render_to_response('import_export.html', d, context_instance=RequestContext(request))


	# Handle file upload
	if request.method == 'POST':
	    form = DocumentForm(request.POST, request.FILES)
	    if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])

			try:
			    importXMLToDjangoFile( newdoc.abspath() + "/static/" +  newdoc.filename(), "static/WorldCrises.xsd.xml")
			    d["success_message"] = "Importing was successful."
			except Exception as e:
			    d["success_message"] = "There was an error when importing:", traceback.format_exc()
	        
	else:
	    form = DocumentForm()  # A empty, unbound form
	    # d['validated'] = True

	d['form'] = form

	# Render list page with the documents and the form
	return render_to_response('import_export.html', d, context_instance=RequestContext(request))


def fileMerge(request):

	d = {}

	password = request.POST['q'].strip()
	if password != "gummypandas":
		d["success_message"] = "Bad password!"
		return render_to_response('import_export.html', d, context_instance=RequestContext(request))

	

	# Handle file upload
	if request.method == 'POST':
	    form = DocumentForm(request.POST, request.FILES)
	    if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])

			try:
			    xmlToDjango( newdoc.abspath() + "/static/" +  newdoc.filename(), "static/WorldCrises.xsd.xml")
			    d["success_message"] = "Merging was successful."
			except Exception as e:
			    d["success_message"] = "There was an error when merging:", traceback.format_exc()
	        
	else:

	    form = DocumentForm()  # A empty, unbound form

	d['form'] = form

	# Render list page with the documents and the form
	return render_to_response('import_export.html', d, context_instance=RequestContext(request))

    
def fileExport(request):
	djangoToXml("static/dbOutput.xml")
	return HttpResponseRedirect("/static/dbOutput.xml")
