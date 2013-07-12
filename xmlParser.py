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
from wcdb.models import Person, Organization, Crisis


# Misc.
import logging




"""
	Parses a XML file into Django models and saves them to the database. 
"""
def xmlToDjango():

	# Uncomment the following lines when hardcoded XML/Schema files are no longer necessary.
	# xmlFilename = raw_input("Filename of the XML file: ")
	# schemaFilename = raw_input("Filename of the schema file: ")
	#xmlFilename = "test/example.xml"
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
def isNotDuplicate (checkID, modelType):

	if modelType == "person":
		getAllObjects = Person.objects.all()
		for currentID in getAllObjects:
			if currentID.PersonID == checkID:
				return False

	if modelType == "crisis":
		getAllObjects = Crisis.objects.all()
		for currentID in getAllObjects:
			if currentID.CrisisID == checkID:
				return False

	if modelType == "org":
		getAllObjects = Organization.objects.all()
		for currentID in getAllObjects:
			if currentID.OrganizationID == checkID:
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
	summary = []

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
def elementTreeToModels(elementTree):

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
					d = getTextAndAttributes(nextElement)
					crisisLocations.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "HumanImpact"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					crisisHumanImpact.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "EconomicImpact"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					crisisEconomicImpact.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "ResourcesNeeded"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					crisisResourcesNeeded.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "WaysToHelp"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					crisisWaysToHelp.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "Common"):
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				crisisCitations = d.get('Citations')
				crisisExternalLinks = d.get('ExternalLinks')
				crisisImages = d.get('Images')
				crisisVideos = d.get('Videos')
				crisisMaps = d.get('Maps')
				crisisFeeds = d.get('Feeds')
				crisisSummary = d.get('Summary')

			if isNotDuplicate(crisisID, "crisis"):
				# crisisAdd = Crisis.objects.create(crisisID = crisisID,
				# 	crisisName = crisisName, crisisKind = crisisKind,
				# 	crisisDate = crisisDate)
				models[0].append(
						Crisis(
						CrisisID = crisisID,
						CrisisName = crisisName,
						crisisKind = crisisKind,
						crisisDate = crisisDate,
						crisisTime = crisisTime,
						#crisisLocation = crisisLocations[0],
						#crisisHumanImpact = crisisHumanImpact[0],
						#crisisEconomicImpact = crisisEconomicImpact[0],
						#crisisResourcesNeeded = crisisResourcesNeeded[0],
						#crisisWaytoHelp = crisisWaysToHelp[0]
						#people = crisisPersonIDs[0],
						#org = crisisOrgIDs[0]
					)
				)

				   
	#c.people = models.ForeignKey('Person', related_name='crisis_people')
	#c.org = models.ForeignKey('Organizations', related_name='crisis_org')
	#c.com = models.ForeignKey('Common', related_name = 'crisis_com')

			#models.append(c)

			
			print "\n\n\n========== CRISIS =========="
			print "crisisID: ", crisisID
			print "crisisName: ", crisisName
			print "crisisPersonIDs = ", crisisPersonIDs
			print "crisisOrgIDs = ", crisisOrgIDs
			print "crisisKind = ", crisisKind
			print "crisisDate = ", crisisDate
			print "crisisTime = ", crisisTime
			print "crisisLocations = ", crisisLocations
			print "crisisHumanImpact = ", crisisHumanImpact
			print "crisisEconomicImpact = ", crisisEconomicImpact
			print "crisisResourcesNeeded = ", crisisResourcesNeeded
			print "crisisWaysToHelp = ", crisisWaysToHelp
			print "\n---- COMMON DATA ----"
			print "crisisCitations = ", crisisCitations
			print "crisisExternalLinks = ", crisisExternalLinks
			print "crisisImages = ", crisisImages
			print "crisisVideos = ", crisisVideos
			print "crisisMaps = ", crisisMaps
			print "crisisFeeds = ", crisisFeeds
			print "crisisSummary = ", crisisSummary

			print "\nnextElement is:", nextElement
		
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
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				personCitations = d.get('Citations')
				personExternalLinks = d.get('ExternalLinks')
				personImages = d.get('Images')
				personVideos = d.get('Videos')
				personMaps = d.get('Maps')
				personFeeds = d.get('Feeds')
				personSummary = d.get('Summary')

			if isNotDuplicate(personID, "person"):
				# personAdd = Person.objects.create(personID = personID,
				#  	personName = personName, personKind = personKind)	
				models[1].append(
					Person(
						PersonID = personID,
						PersonName = personName,
						personKind = personKind,
						personLocation = personLocation
					)
				)
			

	

			print "\n\n\n========== PERSON =========="
			print "personID:", personID
			print "personName:", personName
			print "personCrisisIDs:", personCrisisIDs
			print "personOrgIDs:", personOrgIDs
			print "personKind:", personKind
			print "personLocation:", personLocation
			print "\n---- COMMON DATA ----"
			print "personCitations = ", personCitations
			print "personExternalLinks = ", personExternalLinks
			print "personImages = ", personImages
			print "personVideos = ", personVideos
			print "personMaps = ", personMaps
			print "personFeeds = ", personFeeds
			print "personSummary = ", personSummary

			print "\nnextElement is:", nextElement



		# Parse organizations.
		while (nextElement.tag == "Organization"):

			orgAttributes = getTextAndAttributes(nextElement)
			orgID = orgAttributes['ID']
			orgName = orgAttributes['Name']

			orgCrisisIDs = []
			orgPeopleIDs = []
			orgKind = ""
			orgLocation = ""
			orgHistory = []
			orgContactInfo = []

			orgCitations = []
			orgExternalLinks = []
			orgImages = []
			orgVideos = []
			orgMaps = []
			orgFeeds = []
			orgSummary = ""	

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
				orgKind = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "Location"):
				orgLocation = nextElement.text
				nextElement = treeIter.next()

			if (nextElement.tag == "History"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					orgHistory.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "ContactInfo"):
				nextElement = treeIter.next()
				while (nextElement.tag == "li"):
					d = getTextAndAttributes(nextElement)
					orgContactInfo.append(d)
					nextElement = treeIter.next()


			if (nextElement.tag == "Common"):
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				orgCitations = d.get('Citations')
				orgExternalLinks = d.get('ExternalLinks')
				orgImages = d.get('Images')
				orgVideos = d.get('Videos')
				orgMaps = d.get('Maps')
				orgFeeds = d.get('Feeds')
				orgSummary = d.get('Summary')

			if isNotDuplicate(orgID, "org"):
				# org = Organization.objects.create(orgID = orgID,
				# 	orgName = orgName, orgKind = orgKind,
				# 	orgLocation = orgLocation)
				models[2].append(
					Organization(
						OrganizationID = orgID,
						OrganizationName = orgName,
						orgKind = orgKind,
						orgLocation = orgLocation,
						#orgHistory = orgHistory,
						#orgContact = orgContact
					)
				)
				

			print "\n\n\n========== ORGANIZATION =========="
			print "orgID:", orgID
			print "orgName:", orgName
			print "orgCrisisIDs:", orgCrisisIDs
			print "orgPeopleIDs:", orgPeopleIDs
			print "orgKind:", orgKind
			print "orgLocation:", orgLocation
			print "orgHistory:", orgHistory
			print "orgContactInfo:", orgContactInfo
			print "\n---- COMMON DATA ----"
			print "orgCitations = ", orgCitations
			print "orgExternalLinks = ", orgExternalLinks
			print "orgImages = ", orgImages
			print "orgVideos = ", orgVideos
			print "orgMaps = ", orgMaps
			print "orgFeeds = ", orgFeeds
			print "orgSummary = ", orgSummary

			print "\nnextElement is:", nextElement

			


		nextElement = treeIter.next()

	# Control should normally reach here and return from the function.
	except StopIteration as e:
		print "\nReached end of file correctly!"
		print models
		return models
	"""
	except IntegrityError, e:
   		print "hello"
   		continue
   	"""
	

	# Control should never normally reach here.
	raise IOError("Invalid file!")






"""
	Takes a list of Django models and saves them to a database.
"""
def modelsToDjango(models):

	print "models:", models

	for subList in models:
		for m in subList:
			print "type(m):", type(m)

			# Ensure that every m inherits from django.db.models.Model
			print "m = ", m
			#assert( issubclass(m, models.Model) )
			m.save()


			
		

		
"""
	Parses Django models into a new XML file. 
"""
def djangoToXml():

	outfile = open("static/dbOutput.xml", "w")
	root = ET.Element("WorldCrises")


	for crisis in Crisis.objects.all():

		rootChild = ET.SubElement(root, "Crisis")
		rootChild.set("crisisID", crisis.CrisisID)
		rootChild.set("crisisName", crisis.CrisisName)

		crisisChild = ET.SubElement(rootChild, "Kind")
		crisisChild.text = crisis.crisisKind

		# crisisChild = ET.SubElement(rootChild, "Date")
		# crisisChild.text = crisis.crisisDate

		if (crisis.crisisTime != ""):
			crisisChild = ET.SubElement(rootChild, "Time")
			crisisChild.text = crisis.crisisTime

		# crisisChild = ET.SubElement(rootChild, "Locations")
		# crisisChild.text = crisis.crisisLocations

		# crisisChild = ET.SubElement(rootChild, "HumanImpact")
		# crisisChild.text = crisis.crisisHumanImpact

		# crisisChild = ET.SubElement(rootChild, "EconomicImpact")
		# crisisChild.text = crisis.crisisEconomicImpact

		# crisisChild = ET.SubElement(rootChild, "ResourcesNeeded")
		# crisisChild.text = crisis.crisisResourcesNeeded

		# crisisChild = ET.SubElement(rootChild, "WaysToHelp")
		# crisisChild.text = crisis.crisisWaysToHelp


	for person in Person.objects.all():
		rootChild = ET.SubElement(root, "Person")
		rootChild.set("personID", person.PersonID)
		rootChild.set("personName", person.PersonName)
		
		personChild = ET.SubElement(rootChild, "Kind")
		personChild.text = person.personKind

		# personChild = ET.SubElement(rootChild, "Location")
		# personChild.text = person.personLocation


	for org in Organization.objects.all():
		rootChild = ET.SubElement(root, "Organization")
		rootChild.set("orgID", org.OrganizationID)
		rootChild.set("orgName", org.OrganizationName)

		orgChild = ET.SubElement(rootChild, "Kind")
		orgChild.text = org.orgKind

		orgChild = ET.SubElement(rootChild, "Location")
		orgChild.text = org.orgLocation

		# orgChild = ET.SubElement(rootChild, "History")
		# orgChild.text = org.orgHistory

		# orgChild = ET.SubElement(rootChild, "ContactInfo")
		# orgChild.text = org.orgContactInfo

		
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
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


"""
	Only run this code if not calling 'import'.
"""
if __name__ == "__main__":
	try:
		xmlToDjango()
		djangoToXml();

	except Exception as e:
		logging.exception("Fatal error, ending program. Error message:")

