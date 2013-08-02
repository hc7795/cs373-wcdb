
"""
xmlParser.py
	============

	Contains functions to parse crisis XML files into Django models and vice versa.
"""

# ElementTree XML parsing.
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

# minixsv XML validation and parsing.
from minixsv import pyxsval
from genxmlif import GenXmlIfError

# Setup Django environment.
from django.core.management import setup_environ
import settings
setup_environ(settings)

# Django code.
from django.db import models
from wcdb.models import Person, Organization, Crisis, Common, List


# Misc.
import logging
import sys

#cast a string of ID into list
import ast

from django.template.defaultfilters import slugify


"""
	Parses a XML file into Django models and saves them to the database. 
"""
def xmlToDjango():

	#password = raw_input("Password: ")
	#if (password != "gummy"):
	#	print "Bad password!"
	#	exit(1)


	#xmlFilename = raw_input("Filename of the XML file: ")
	#schemaFilename = raw_input("Filename of the schema file: ")
	xmlFilename = "static/WorldCrises.xml"
	schemaFilename = "static/WorldCrises.xsd.xml"


	# Validate the XML file.
	try:

		# call validator with non-default values
		elementTreeWrapper = pyxsval.parseAndValidate (xmlFilename, 
			xsdFile         = schemaFilename,
			xmlIfClass      = pyxsval.XMLIF_ELEMENTTREE,
			warningProc     = pyxsval.PRINT_WARNINGS,
			errorLimit      = 200, 
			verbose         = 1,
			useCaching      = 0, 
			processXInclude = 0)

		# get elementtree object after validation
		xmlTree = elementTreeWrapper.getTree()


	except pyxsval.XsvalError as errstr:
		print errstr
		print "Validation aborted!"
		raise pyxsval.XsvalError

	except GenXmlIfError as errstr:
		print errstr
		print "Parsing aborted!"
		raise GenXmlIfError

	# Get a list of model objects from xmlTree.
	modelsList = elementTreeToModels(xmlTree)

	# Put the models in the Django database.
	modelsToDjango(modelsList)



"""
	Takes an elementTree element and returns a dictionary containing attribute_id/attribute_data pairs.
	Also returns a pair with the key called 'content', which contains text (if any) of the element.
"""
def getTextAndAttributes(element):
	d = {}
	for pair in element.items():
		d[pair[0]] = pair[1]

	content = element.text
	# check the existence of text
	if (content != None and content.strip() != ''):
		d['content'] = content

	return d


"""
	take an ID and check to see if that ID is already in Crisis/Person/Organization or not
"""
def isNotDuplicate (checkID, modelType, unitTestDB = "No"):

	if unitTestDB == "No":
		if modelType == "person":
			getAllObjects = Person.objects.all()
			for currentID in getAllObjects:
				if currentID.id == checkID:
					return False

		if modelType == "crisis":
			getAllObjects = Crisis.objects.all()
			for currentID in getAllObjects:
				if currentID.id == checkID:
					return False

		if modelType == "org":
			getAllObjects = Organization.objects.all()
			for currentID in getAllObjects:
				if currentID.id == checkID:
					return False

	else:
		for key in unitTestDB:
			if checkID in unitTestDB.values():
				return False


	return True



"""
	Takes a 'Common' element and returns a tuple (r1, r2, r3).
	r1: the current element pointed to by element iterator after iteration.
	r2: the element iterator after iteration.
	r3: dictionary containing its nested data.
"""
def getCommonData(element, elementIterator):
	assert(element.tag == "Common")

	returnData = {}

	locations = []
	humanImpact = []
	economicImpact = []
	resourcesNeeded = []
	waysToHelp = []
	citations = []
	externalLinks = []
	images = []
	videos = []
	maps = []
	feeds = []
	summary = ""

	try:
		nextElement = elementIterator.next()

		if (nextElement.tag == "Citations"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				citations.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "ExternalLinks"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				externalLinks.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "Images"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				images.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "Videos"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				videos.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "Maps"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				maps.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "Feeds"):
			nextElement = elementIterator.next()
			while (nextElement.tag == "li"):
				d = getTextAndAttributes(nextElement)
				feeds.append(d)
				nextElement = elementIterator.next()

		if (nextElement.tag == "Summary"):
			summary = nextElement.text
			nextElement = elementIterator.next()

	# It's possible the end of file might be reached. If so, still continue and return the data.
	except StopIteration as e:
		pass

	finally:
		returnData["Citations"] = citations
		returnData["ExternalLinks"] = externalLinks
		returnData["Images"] = images
		returnData["Videos"] = videos
		returnData["Maps"] = maps
		returnData["Feeds"] = feeds
		returnData["Summary"] = summary

	return (nextElement, elementIterator, returnData)



"""
	Parses an XML file and returns a list of Django models.
"""
def elementTreeToModels(elementTree, unitTestDB = "No"):

	treeIter = elementTree.iter()
	models = []

	crisisModels = []
	personModels = []
	orgModels = []

	models.append(crisisModels)
	models.append(personModels)
	models.append(orgModels)


	nextElement = treeIter.next() # Retrieves root element
	nextElement = treeIter.next() # Retrieves next Crisis element


	try:
		# Parse crises. 
		while (nextElement.tag == "Crisis"):
			crisisAttributes = getTextAndAttributes(nextElement)
			crisisID = crisisAttributes['ID']
			crisisName = crisisAttributes['Name']

			crisisPersonIDs = []
			crisisOrgIDs = []
			crisisKind = ""
			crisisDate = ""
			crisisTime = ""
			crisisLocations = []
			crisisHumanImpact = []
			crisisEconomicImpact = []
			crisisResourcesNeeded = []
			crisisWaysToHelp = []

			crisisCitations = []
			crisisExternalLinks = []
			crisisImages = []
			crisisVideos = []
			crisisMaps = []
			crisisFeeds = []
			crisisSummary = ""
			commonExists=False


			nextElement = treeIter.next() # People element
			if (nextElement.tag == "People"):
				nextElement = treeIter.next() # First Person in People sequence
				while (nextElement.tag == "Person"):
					crisisPersonIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "Organizations"):
				nextElement = treeIter.next()
				while (nextElement.tag == "Org"):
					crisisOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "Kind"):
				crisisKind = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "Date"):
				crisisDate = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "Time"):
				crisisTime = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "Locations"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					crisisLocations.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "HumanImpact"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					crisisHumanImpact.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "EconomicImpact"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					crisisEconomicImpact.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "ResourcesNeeded"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					crisisResourcesNeeded.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "WaysToHelp"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					crisisWaysToHelp.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "Common"):
				commonExists=True
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				crisisCitations = d.get('Citations')
				crisisExternalLinks = d.get('ExternalLinks')
				crisisImages = d.get('Images')
				crisisVideos = d.get('Videos')
				crisisMaps = d.get('Maps')
				crisisFeeds = d.get('Feeds')
				crisisSummary = d.get('Summary')
			

			#if isNotDuplicate(crisisID, "crisis", unitTestDB):
			# Common
			if (commonExists==False):
				common=None
				#common.save()
			else:
				common=	Common()
				if(crisisSummary != "") :
				  common.summary= crisisSummary
				common.save()
				for c in crisisCitations:
					li=List()
					li.href=c.get("href")
					li.embed=c.get("embed")
					li.text=c.get("text")
					li.content=c.get("content")
					li.save()
					common.citations.add(li)

				for c in crisisExternalLinks:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.externalLinks.add(li)

				for c in crisisImages:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.images.add(li)

				for c in crisisVideos:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.videos.add(li)
				for c in crisisMaps:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.maps.add(li)
				for c in crisisFeeds:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.feeds.add(li)


			models[0].append(
					Crisis(
					id = crisisID,
					name = crisisName,
					kind = crisisKind,
					date = crisisDate,
					time = crisisTime,
					people = str(crisisPersonIDs),
					organizations = str(crisisOrgIDs),
					location = str(crisisLocations),
					humanImpact = str(crisisHumanImpact),
					economicImpact = str(crisisEconomicImpact),
					resourcesNeeded = str(crisisResourcesNeeded),
					waytoHelp = str(crisisWaysToHelp),						
					common = common,
					slug = slugify(crisisName),
					)
			)

		# Parse people. 
		
		while (nextElement.tag == "Person"):
			personAttributes = getTextAndAttributes(nextElement)
			personID = personAttributes['ID']
			personName = personAttributes['Name']

			personCrisisIDs = []
			personOrgIDs = []
			personKind = ""
			personLocation = ""

			personCitations = []
			personExternalLinks = []
			personImages = []
			personVideos = []
			personMaps = []
			personFeeds = []
			personSummary = ""
			commonExists = False

			nextElement = treeIter.next() 

			if (nextElement.tag == "Crises"):
				nextElement = treeIter.next() # First Crisis in Crises sequence
				while (nextElement.tag == "Crisis"):
					personCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "Organizations"):
				nextElement = treeIter.next() # First Org in Organizations sequence
				while (nextElement.tag == "Org"):
					personOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "Kind"):
				personKind = nextElement.text # Kind text
				nextElement = treeIter.next()

			if (nextElement.tag == "Location"):
				personLocation = nextElement.text # Location text
				nextElement = treeIter.next()

			if (nextElement.tag == "Common"):
				commonExists = True
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				personCitations = d.get('Citations')
				personExternalLinks = d.get('ExternalLinks')
				personImages = d.get('Images')
				personVideos = d.get('Videos')
				personMaps = d.get('Maps')
				personFeeds = d.get('Feeds')
				personSummary = d.get('Summary')

			#if isNotDuplicate(personID, "person", unitTestDB):
			if (commonExists == False):
				common=None
			else:
				common=	Common()
				if(personSummary != "") :
				  common.summary= personSummary
				common.save()
				for c in personCitations:
					li=List()
					li.href=c.get("href")
					li.embed=c.get("embed")
					li.text=c.get("text")
					li.content=c.get("content")
					li.save()
					common.citations.add(li)

				for c in personExternalLinks:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.externalLinks.add(li)

				for c in personImages:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.images.add(li)

				for c in personVideos:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.videos.add(li)
				for c in personMaps:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.maps.add(li)
				for c in personFeeds:
					li=List(
					href=c.get("href"),
					embed=c.get("embed"),
					text=c.get("text"),
					content=c.get("content")
					)
					li.save()
					common.feeds.add(li)

			models[1].append(
				Person(
					id = personID,
					name = personName,
					kind = personKind,
					location = personLocation,
					crises=str(personCrisisIDs),
					organizations=str(personOrgIDs),
					common = common,
					slug = slugify(personName),
				)
			)

		# Parse organizations.
		while (nextElement.tag == "Organization"):

			orgAttributes = getTextAndAttributes(nextElement)
			orgID = orgAttributes['ID']
			orgName = orgAttributes['Name']

			orgCrisisIDs = []
			orgPeopleIDs = []
			kind = ""
			location = ""
			history = []
			contactInfo = []

			orgCitations = []
			orgExternalLinks = []
			orgImages = []
			orgVideos = []
			orgMaps = []
			orgFeeds = []
			orgSummary = ""
			commonExists = False

			nextElement = treeIter.next()
			


			if (nextElement.tag == "Crises"):
				nextElement = treeIter.next()
				while (nextElement.tag == "Crisis"):
					orgCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "People"):
				nextElement = treeIter.next() 
				while (nextElement.tag == "Person"):
					orgPeopleIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "Kind"):
				kind = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "Location"):
				location = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "History"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					history.append(nextElement.text)
					nextElement = treeIter.next()

			if (nextElement.tag == "ContactInfo"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					contactInfo.append(nextElement.text)
					nextElement = treeIter.next()


			if (nextElement.tag == "Common"):
				commonExists = True
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				orgCitations = d.get('Citations')
				orgExternalLinks = d.get('ExternalLinks')
				orgImages = d.get('Images')
				orgVideos = d.get('Videos')
				orgMaps = d.get('Maps')
				orgFeeds = d.get('Feeds')
				orgSummary = d.get('Summary')
				
			if (commonExists == False):
					common=None
			else:
					common=	Common()
					if(orgSummary != "") :
					  common.summary= orgSummary
					common.save()
					for c in orgCitations:
						li=List()
						li.href=c.get("href")
						li.embed=c.get("embed")
						li.text=c.get("text")
						li.content=c.get("content")
						li.save()
						common.citations.add(li)

					for c in orgExternalLinks:
						li=List(
						href=c.get("href"),
						embed=c.get("embed"),
						text=c.get("text"),
						content=c.get("content")
						)
						li.save()
						common.externalLinks.add(li)

					for c in orgImages:
						li=List(
						href=c.get("href"),
						embed=c.get("embed"),
						text=c.get("text"),
						content=c.get("content")
						)
						li.save()
						common.images.add(li)

					for c in orgVideos:
						li=List(
						href=c.get("href"),
						embed=c.get("embed"),
						text=c.get("text"),
						content=c.get("content")
						)
						li.save()
						common.videos.add(li)
					for c in orgMaps:
						li=List(
						href=c.get("href"),
						embed=c.get("embed"),
						text=c.get("text"),
						content=c.get("content")
						)
						li.save()
						common.maps.add(li)
					for c in orgFeeds:
						li=List(
						href=c.get("href"),
						embed=c.get("embed"),
						text=c.get("text"),
						content=c.get("content")
						)
						li.save()
						common.feeds.add(li)


			#if isNotDuplicate(orgID, "org", unitTestDB):
			models[2].append(
				Organization(
					id = orgID,
					name = orgName,
					kind = kind,
					location = location,
					history = history,
					contact = contactInfo,
					crises=str(orgCrisisIDs),
					people=str(orgPeopleIDs),
					common = common,
					slug = slugify(orgName),
				)
			)

		nextElement = treeIter.next()

	# Control should normally reach here and return from the function.
	except StopIteration as e:
		#print "\nReached end of file correctly!"
		#print models
		return models
	"""
	except IntegrityError, e:
   		print "hello"
   		continue
   	"""


	# Control should never normally reach here.
	raise IOError("Invalid file!")





def merge(c, m):
	pass



"""
	Takes a list of Django models and saves them to a database.
"""
def modelsToDjango(models):
	
	crises = models[0]
	people = models[1]
	orgs =   models[2]
	count=1;
	print "elements of model[0] ",crises
	for m in crises:
		checkExistence = Crisis.objects.filter(id=m.id).count()
		if checkExistence == 1:
			#append images from m to c
			# ... ditto for rest of attributes
			print count
			count+=1
			c=Crisis.objects.get(id = m.id)
			merge(c, m)
			c.save()
		elif checkExistence == 0:
			print "save",m.id
			m.save()
		else:
			print "something wrong"






"""
	Parses Django models into a new XML file. 
"""
def djangoToXml():

	outfile = open("static/dbOutput.xml", "w")
	root = ET.Element("WorldCrises")


	for crisis in Crisis.objects.all():

		rootChild = ET.SubElement(root, "Crisis")
		rootChild.set("crisisID", crisis.id)
		rootChild.set("crisisName", crisis.name)

		#People ID
		crisis_person_str=crisis.people
		crisis_person_list=ast.literal_eval(crisis_person_str)
		rootChild2 = ET.SubElement(rootChild, "People")
		for cp in crisis_person_list:
			rootChild3 = ET.SubElement(rootChild2, "Person")
			rootChild3.set("ID", cp)


		#Organization ID
		crisis_Organization_str=crisis.organizations
		crisis_Organization_list=ast.literal_eval(crisis_Organization_str)
		rootChild2 = ET.SubElement(rootChild, "Organizations")
		for co in crisis_Organization_list:
			rootChild3 = ET.SubElement(rootChild2, "Org")
			rootChild3.set("ID", co)

		#Kind
		if(crisis.kind) :
			crisisChild = ET.SubElement(rootChild, "Kind")
			crisisChild.text = crisis.kind

		#Time
		if (crisis.time):
			crisisChild = ET.SubElement(rootChild, "Time")
			crisisChild.text = crisis.time

		#Date	
		if (crisis.date):
			crisisChild = ET.SubElement(rootChild, "Date")
			crisisChild.text = crisis.date

		#Location
		crisis_Location_str=crisis.location
		crisis_Location_list=ast.literal_eval(crisis_Location_str)
		if(crisis_Location_list) :
			rootChild2 = ET.SubElement(rootChild, "Locations")
			for cl in crisis_Location_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = cl

		#crisisHumanImpact
		crisis_HumanImpact_str=crisis.humanImpact
		crisis_HumanImpact_list=ast.literal_eval(crisis_HumanImpact_str)
		if(crisis_HumanImpact_list) :
			rootChild2 = ET.SubElement(rootChild, "HumanImpact")
			for ch in crisis_HumanImpact_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = ch

		#crisisEconomicImpact
		crisis_EconomicImpact_str=crisis.economicImpact
		crisis_EconomicImpact_list=ast.literal_eval(crisis_EconomicImpact_str)
		if(crisis_EconomicImpact_list) :	
			rootChild2 = ET.SubElement(rootChild, "EconomicImpact")
			for ce in crisis_EconomicImpact_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = ce

		#crisisResourcesNeeded
		crisis_ResourcesNeeded_str=crisis.resourcesNeeded
		crisis_ResourcesNeeded_list=ast.literal_eval(crisis_ResourcesNeeded_str)
		if(crisis_ResourcesNeeded_list) :
			rootChild2 = ET.SubElement(rootChild, "ResourcesNeeded")
			for cr in crisis_ResourcesNeeded_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = cr

		#crisisWayToHelp
		crisis_WaytoHelp_str=crisis.waytoHelp
		crisis_WaytoHelp_list=ast.literal_eval(crisis_WaytoHelp_str)
		if(crisis_WaytoHelp_list) :
			rootChild2 = ET.SubElement(rootChild, "WaysToHelp")
			for cw in crisis_WaytoHelp_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = cw


		#Common
		if(crisis.common!=None):
			crisisChild = ET.SubElement(rootChild, "Common")
			if(crisis.common.citations.exists()):
				commonChild=ET.SubElement(crisisChild,"Citations")
				for li in crisis.common.commonCitations.all():
					CitationsChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						CitationsChild.set("href",li.href)
					if(li.embed!=None):
						CitationsChild.set("embed",li.embed)
					if(li.text!=None):
						CitationsChild.set("text",li.text)
					if(li.content!=None):
						CitationsChild.text=li.content

			if(crisis.common.externalLinks.exists()):
				commonChild=ET.SubElement(crisisChild,"ExternalLinks")
				for li in crisis.common.externalLinks.all():
					ExternalLinksChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ExternalLinksChild.set("href",li.href)
					if(li.embed!=None):
						ExternalLinksChild.set("embed",li.embed)
					if(li.text!=None):
						ExternalLinksChild.set("text",li.text)
					if(li.content!=None):
						ExternalLinksChild.text=li.content

			if(crisis.common.images.exists()):
				commonChild=ET.SubElement(crisisChild,"Images")
				for li in crisis.common.images.all():
					ImagesChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ImagesChild.set("href",li.href)
					if(li.embed!=None):
						ImagesChild.set("embed",li.embed)
					if(li.text!=None):
						ImagesChild.set("text",li.text)
					if(li.content!=None):
						ImagesChild.text=li.content
			if(crisis.common.summary != None):
				commonChild=ET.SubElement(crisisChild,"Summary")
				crisisChild.text = crisis.common.summary



	for person in Person.objects.all():
		rootChild = ET.SubElement(root, "Person")
		rootChild.set("personID", person.id)
		rootChild.set("personName", person.name)

		#Location
		if(person.location):
			personChild = ET.SubElement(rootChild, "Location")
			personChild.text = person.location

		#Crisis ID
		person_crisis_str=person.crises
		person_crisis_list=ast.literal_eval(person_crisis_str)
		rootChild2 = ET.SubElement(rootChild, "Crises")
		for pc in person_crisis_list:
			rootChild3 = ET.SubElement(rootChild2, "Crisis")
			rootChild3.set("ID", pc)	

		#Organization ID
		person_Organization_str = person.organizations
		person_Organization_list = ast.literal_eval(person_Organization_str)
		rootChild2 = ET.SubElement(rootChild, "Organizations")
		for po in person_Organization_list:
			rootChild3 = ET.SubElement(rootChild2, "Org")
			rootChild3.set("ID", po)

		#kind
		if(person.kind):
			personChild = ET.SubElement(rootChild, "Kind")
			personChild.text = person.kind

		#Common
		if(person.common!=None):
			personChild = ET.SubElement(rootChild, "Common")
			if(person.common.citations.exists()):
				commonChild=ET.SubElement(personChild,"Citations")
				for li in person.common.citations.all():
					CitationsChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						CitationsChild.set("href",li.href)
					if(li.embed!=None):
						CitationsChild.set("embed",li.embed)
					if(li.text!=None):
						CitationsChild.set("text",li.text)
					if(li.content!=None):
						CitationsChild.text=li.content

			if(person.common.externalLinks.exists()):
				commonChild=ET.SubElement(personChild,"ExternalLinks")
				for li in person.common.externalLinks.all():
					ExternalLinksChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ExternalLinksChild.set("href",li.href)
					if(li.embed!=None):
						ExternalLinksChild.set("embed",li.embed)
					if(li.text!=None):
						ExternalLinksChild.set("text",li.text)
					if(li.content!=None):
						ExternalLinksChild.text=li.content

			if(person.common.images.exists()):
				commonChild=ET.SubElement(personChild,"Images")
				for li in person.common.images.all():
					ImagesChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ImagesChild.set("href",li.href)
					if(li.embed!=None):
						ImagesChild.set("embed",li.embed)
					if(li.text!=None):
						ImagesChild.set("text",li.text)
					if(li.content!=None):
						ImagesChild.text=li.content
			if(person.common.summary != None):
				commonChild=ET.SubElement(personChild,"Summary")
				personChild.text = person.common.summary


	for org in Organization.objects.all():
		rootChild = ET.SubElement(root, "Organization")
		rootChild.set("orgID", org.id)
		rootChild.set("orgName", org.name)

		#OrganizationCrisis
		org_crisis_str=org.crises
		org_crisis_list=ast.literal_eval(org_crisis_str)
		rootChild2 = ET.SubElement(rootChild, "Crises")
		for oc in org_crisis_list:
			rootChild3 = ET.SubElement(rootChild2, "Crisis")
			rootChild3.set("ID", oc)

		#OrganizationPerson
		org_OrganizationPerson_str=org.people
		org_OrganizationPerson_list=ast.literal_eval(org_OrganizationPerson_str)
		rootChild2 = ET.SubElement(rootChild, "People")
		for op in org_OrganizationPerson_list:
			rootChild3 = ET.SubElement(rootChild2, "Person")
			rootChild3.set("ID", op)

		#kind
		if(org.kind) :
			orgChild = ET.SubElement(rootChild, "Kind")
			orgChild.text = org.kind

		#Location
		if(org.location) :
			orgChild = ET.SubElement(rootChild, "Location")
			orgChild.text = org.location

		#orgHistory
		org_orgHistory_str=org.history
		org_orgHistory_list=ast.literal_eval(org_orgHistory_str)
		if(org_orgHistory_list) :
			rootChild2 = ET.SubElement(rootChild, "History")
			for oh in org_orgHistory_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = oh

		#orgContact
		org_orgContact_str=org.contact
		org_orgContact_list=ast.literal_eval(org_orgContact_str)
		if(org_orgContact_list) :
			rootChild2 = ET.SubElement(rootChild, "ContactInfo")
			for oc in org_orgContact_list:
				rootChild3 = ET.SubElement(rootChild2, "li")
				rootChild3.text = oc

		#Common
		if(org.common!=None):
			orgChild = ET.SubElement(rootChild, "Common")
			if(org.common.citations.exists()):
				commonChild=ET.SubElement(orgChild,"Citations")
				for li in org.common.citations.all():
					CitationsChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						CitationsChild.set("href",li.href)
					if(li.embed!=None):
						CitationsChild.set("embed",li.embed)
					if(li.text!=None):
						CitationsChild.set("text",li.text)
					if(li.content!=None):
						CitationsChild.text=li.content

			if(org.common.externalLinks.exists()):
				commonChild=ET.SubElement(orgChild,"ExternalLinks")
				for li in org.common.externalLinks.all():
					ExternalLinksChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ExternalLinksChild.set("href",li.href)
					if(li.embed!=None):
						ExternalLinksChild.set("embed",li.embed)
					if(li.text!=None):
						ExternalLinksChild.set("text",li.text)
					if(li.content!=None):
						ExternalLinksChild.text=li.content

			if(org.common.images.exists()):
				commonChild=ET.SubElement(orgChild,"Images")
				for li in org.common.images.all():
					ImagesChild=ET.SubElement(commonChild,"li")
					if(li.href!=None):
						ImagesChild.set("href",li.href)
					if(li.embed!=None):
						ImagesChild.set("embed",li.embed)
					if(li.text!=None):
						ImagesChild.set("text",li.text)
					if(li.content!=None):
						ImagesChild.text=li.content
			if(org.common.summary != None):
				commonChild=ET.SubElement(orgChild,"Summary")
				orgChild.text = org.common.summary



	indent(root)
	tree = ET.ElementTree(root)

	tree.write(outfile, method="xml")
	outfile.close()


"""
	Adds indention to an ElementTree element. Written by Fredrik Lundh.
"""
def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



"""
	Only run this code if not calling 'import'.
"""
if __name__ == "__main__":
	try:
		if len(sys.argv) == 2:
			if sys.argv[1] == "import":
				xmlToDjango()
				exit(0)
			elif sys.argv[1] == "export":
				djangoToXml()
				exit(0)

		print "\nHow to use:\n\n\tReading from XML to database:\n\txmlParser.py import\n\n\tWriting database to XML:\n\txmlParser.py output\n"

	except IOError as ioe:
		print "Error parsing files!"

	except Exception as e:
		logging.exception("Fatal error, ending program. Error message:")
