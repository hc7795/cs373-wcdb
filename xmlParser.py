"""
	xmlParser.py
	============

	Contains functions to parse crisis XML files into Django models and vice versa.
"""

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from minixsv import pyxsval
from genxmlif import GenXmlIfError

import logging





"""
	Driver function.
"""
def main():
	try:
		xmlToDjango()

	except Exception as e:
		logging.exception("Fatal error, ending program. Error message:")





"""
	Parses a XML file into Django models and saves them to the database. 
"""
def xmlToDjango():

	# Uncomment the following lines when hardcoded XML/Schema files are no longer necessary.
	# xmlFilename = raw_input("Filename of the XML file: ")
	# schemaFilename = raw_input("Filename of the schema file: ")
	xmlFilename = "test/example.xml"
	schemaFilename = "test/schema.xml"

	# Validate the XML file.
	try:

		# call validator with non-default values
		elementTreeWrapper = pyxsval.parseAndValidate (xmlFilename, 
			xsdFile=schemaFilename,
			xmlIfClass= pyxsval.XMLIF_ELEMENTTREE,
			warningProc=pyxsval.PRINT_WARNINGS,
			errorLimit=200, 
			verbose=1,
			useCaching=0, 
			processXInclude=0)

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
    if (content != ""):
	d['content'] = content
    return d



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

	nextElement = elementIterator.next()

	if(nextElement.tag == "Citations") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    citations.append(d)
		    nextElement = elementIterator.next()
		returnData["Citations"] = citations

	if(nextElement.tag == "ExternalLinks") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    externalLinks.append(d)
		    nextElement = elementIterator.next()
		returnData["ExternalLinks"] = externalLinks

	if(nextElement.tag == "Images") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    images.append(d)
		    nextElement = elementIterator.next()
		returnData["Images"] = images

	if(nextElement.tag == "Videos") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    videos.append(d)
		    nextElement = elementIterator.next()
		returnData["Videos"] = videos

	if(nextElement.tag == "Maps") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    maps.append(d)
		    nextElement = elementIterator.next()
		returnData["Maps"] = maps

	if(nextElement.tag == "Feeds") :
		nextElement = elementIterator.next()
		while(nextElement.tag == "li"):
		    d=getTextAndAttributes(nextElement)
		    feeds.append(d)
		    nextElement = elementIterator.next()
		returnData["Feeds"] = feeds

	if(nextElement.tag == "Summary") :
		crisisSummary=nextElement.text
		returnData["Summary"] = crisisSummary
		nextElement = elementIterator.next()

	return (nextElement, elementIterator, returnData)





"""
	Parses an XML file and returns a list of Django models.
"""
def elementTreeToModels(elementTree):

	treeIter = elementTree.iter()


	nextElement = treeIter.next() # Retrieves root element
	print nextElement
	nextElement = treeIter.next() # Retrieves next Crisis element
	print nextElement

	try:
<<<<<<< HEAD
   	 # Parse crises.    
   	        while (nextElement.tag == "Crisis"):
   		        crisisAttributes = getTextAndAttributes(nextElement)
			crisisID = crisisAttributes['ID']
			crisisName = crisisAttributes['Name']


   		        # print crisisAttributes
   			print crisisID
   			print crisisName
   		 
   			crisisPersonIDs = []
   			crisisOrgIDs = []
   			crisisKind = ""
   			crisisDate = ""
=======
		# Parse crises. 
		while (nextElement.tag == "Crisis"):
			crisisAttributes = nextElement.items()
			crisisID = [pair[1] for pair in crisisAttributes if pair[0] == "ID"][0]
			crisisName = [pair[1] for pair in crisisAttributes if pair[0] == "Name"][0]

			crisisPersonIDs = []
			crisisOrgIDs = []
			crisisKind = ""
			crisisDate = ""
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7
			crisisTime = ""
			crisisLocations = []
			crisisHumanImpact = []
			crisisEconomicImpact = []
<<<<<<< HEAD
   			crisisResourcesNeeded = []
   		 	crisisWaysToHelp = []
 
=======
			crisisResourcesNeeded = []
			crisisWaysToHelp = []
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7
			crisisCitations = []
			crisisExternalLinks = []
			crisisImages = []
			crisisVideos = []
			crisisMaps = []
			crisisFeeds = []
<<<<<<< HEAD
			crisisSummary = ""		 

   		        nextElement = treeIter.next() # People element
   		 	if(nextElement.tag == "People") :
   		 	    nextElement = treeIter.next() # First Person in People sequence
   		 	    while (nextElement.tag == "Person"):
   			        crisisPersonIDs.append(nextElement.attrib['ID'])
   		     	        nextElement = treeIter.next()

   		        if(nextElement.tag == "Organizations") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "Org") :
   			        crisisOrgIDs.append(nextElement.attrib['ID'])
   			        nextElement = treeIter.next()
   						 
   		 	if(nextElement.tag == "Kind") :
   		 	    crisisKind = nextElement.text
   		 	    nextElement = treeIter.next()
   			 
   		 	if(nextElement.tag == "Date") :
   		 	    crisisDate = nextElement.text
   		 	    nextElement = treeIter.next()

   		 	if(nextElement.tag == "Time") :
   		 	    crisisTime = nextElement.text
   		 	    nextElement = treeIter.next()

   		        if(nextElement.tag == "Locations") :
   		 	    nextElement = treeIter.next()
			    while(nextElement.tag == "li") :
				d=getTextAndAttributes(nextElement)
			        crisisLocations.append(d)
=======
			crisisSummary = [] 

			nextElement = treeIter.next() # People element
			if(nextElement.tag == "People") :
				nextElement = treeIter.next() # First Person in People sequence
				while (nextElement.tag == "Person"):
					crisisPersonIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if(nextElement.tag == "Organizations") :
				nextElement = treeIter.next()
				while(nextElement.tag == "Org") :
					crisisOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
					
			if(nextElement.tag == "Kind") :
				crisisKind = nextElement.text
				nextElement = treeIter.next()
			
			if(nextElement.tag == "Date") :
				crisisDate = nextElement.text
				nextElement = treeIter.next()

			if(nextElement.tag == "Time") :
				crisisTime = nextElement.text
				nextElement = treeIter.next()

		   	if(nextElement.tag == "Locations") :
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					crisisLocations.append(nextElement.text)
					nextElement = treeIter.next()

			if(nextElement.tag == "HumanImpact") :
<<<<<<< HEAD
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
				d=getTextAndAttributes(nextElement)
			        crisisHumanImpact.append(d)
=======
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					crisisHumanImpact.append(nextElement.text)
					nextElement = treeIter.next()

			if(nextElement.tag == "EconomicImpact") :
<<<<<<< HEAD
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
				d=getTextAndAttributes(nextElement)
			        crisisEconomicImpact.append(d)
=======
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					crisisEconomicImpact.append(nextElement.text)
					nextElement = treeIter.next()

			if(nextElement.tag == "ResourcesNeeded") :
<<<<<<< HEAD
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
				    d=getTextAndAttributes(nextElement)
				    crisisResourcesNeeded.append(d)
				    nextElement = treeIter.next()

			if(nextElement.tag == "WaysToHelp") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
				    d=getTextAndAttributes(nextElement)
				    crisisWaysToHelp.append(d)
				    nextElement = treeIter.next()

			if(nextElement.tag == "Common") :
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				crisisCitations = d.get('Citations')
				crisisExternalLinks = d.get('Links')
				crisisImages = d.get('Images')
				crisisVideos = d.get('Videos')
				crisisMaps = d.get('Maps')
				crisisFeeds = d.get('Feeds')
				crisisSummary = d.get('Summary')
				
=======
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					crisisResourcesNeeded.append(nextElement.text)
					nextElement = treeIter.next()

			if(nextElement.tag == "WaysToHelp") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					crisisWaysToHelp.append(nextElement.text)
					crisisWaysToHelp.append(nextElement.attrib)
					nextElement = treeIter.next()

			if(nextElement.tag == "Common") :
				nextElement = treeIter.next()

			if(nextElement.tag == "Citations") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					content = nextElement.text
					# check the existence of text
					if (content != ""):
						dict['content']=content
					crisisCitations.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "ExternalLinks") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					crisisExternalLinks.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "Images") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					crisisImages.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "Videos") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					crisisVideos.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "Maps") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					crisisMaps.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "Feeds") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
					dict={}
					ExternalAttributes = nextElement.items()
					ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"]
					ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"]
					ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"]
					if(ExternalAttHref != []):
						dict['href'] =ExternalAttHref[0]
					if(ExternalAttEmbed != []):
						dict['embed'] =ExternalAttEmbed[0]
					if(ExternalAttText != []):
						dict['text'] =ExternalAttText[0]
					crisisFeeds.append(dict)
					nextElement = treeIter.next()

			if(nextElement.tag == "Summary") :
				crisisSummary=nextElement.text
				nextElement = treeIter.next()
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7

			
			print "----- crisis -----"
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
			print "crisisCitations = ", crisisCitations
			print "crisisExternalLinks = ", crisisExternalLinks
			print "crisisImages = ", crisisImages
			print "crisisVideos = ", crisisVideos
			print "crisisMaps = ", crisisMaps
			print "crisisFeeds = ", crisisFeeds
			print "crisisSummary = ", crisisSummary
		
		# Parse people. 
		while (nextElement.tag == "Person"):

			personAttributes = nextElement.items()
			personID = [pair[1] for pair in personAttributes if pair[0] == "ID"][0]
			personName = [pair[1] for pair in personAttributes if pair[0] == "Name"][0]

			personCrisisIDs = []
			personOrgIDs = []
			personKind = ""
			personLocation = ""

			nextElement = treeIter.next() 

			if (nextElement.tag == "Crises"):
				nextElement = treeIter.next() # First Crisis in Crises sequence
				while (nextElement.tag == "Crisis"):
					personCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
				
			if (nextElement.tag == "Organizations"):
				nextElement = treeIter.next() # First Org in Organizations sequence
				while(nextElement.tag == "Org"):
					personOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
			
			if (nextElement.tag == "Kind"):
				personKind = nextElement.text # Kind text
				nextElement = treeIter.next()
			
			if (nextElement.tag == "Location"):
				personLocation = nextElement.text # Location text
				nextElement = treeIter.next()

			print "----- person -----"
			print "personID:", personID
			print "personName:", personName
			print "personCrisisIDs:", personCrisisIDs
			print "personOrgIDs:", personOrgIDs
			print "personKind:", personKind
			print "personLocation:", personLocation


		# Parse organizations.
		while (nextElement.tag == "Organization"):

			orgAttributes = nextElement.items()
			orgID = [pair[1] for pair in orgAttributes if pair[0] == "ID"][0]
			orgName = [pair[1] for pair in orgAttributes if pair[0] == "Name"][0]

			orgCrisisIDs = []
			orgPeopleIDs = []
			orgContactInfo = []

<<<<<<< HEAD
	    
		# Parse people.	
		while (nextElement.tag == "Person"):
			print 'nextElement.tag == "Person":', nextElement.tag == "Person"

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
=======
			nextElement = treeIter.next()
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7

			if (nextElement.tag == "Crises"):
				nextElement = treeIter.next() # First Crisis in Crises sequence
				while (nextElement.tag == "Crisis"):
<<<<<<< HEAD
					personCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
				
			if (nextElement.tag == "Organizations"):
				nextElement = treeIter.next() # First Org in Organizations sequence
				while(nextElement.tag == "Org"):
					personOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
			
			if (nextElement.tag == "Kind"):
				personKind = nextElement.text # Kind text
				nextElement = treeIter.next()
			
			if (nextElement.tag == "Location"):
				personLocation = nextElement.text # Location text
				nextElement = treeIter.next()
=======
					orgCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()

			if (nextElement.tag == "People"):
				nextElement = treeIter.next() # First Crisis in Crises sequence
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
				orgHistory = nextElement.text
				nextElement = treeIter.next()

			print "----- organization -----"
			print "orgID:", orgID
			print "orgName:", orgName
			print "orgCrisisIDs:", orgCrisisIDs
			print "orgPeopleIDs:", orgPeopleIDs
			print "orgKind:", orgKind
			print "orgLocation:", orgLocation
			print "orgHistory:", orgHistory

			if (nextElement.tag == "ContactInfo"):
				nextElement = treeIter.next() 
				while (nextElement.tag == "li"):
					orgContactInfo.append(nextElement.text)
					print "orgContactInfo:", orgContactInfo
					nextElement = treeIter.next()
			


			#print "orgContactInfo:", orgContactInfo
>>>>>>> 7178e45c9a36df06ecfc44fadc92aace207031f7

			if(nextElement.tag == "Common") :
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				personCitations = d.get('Citations')
				personExternalLinks = d.get('Links')
				personImages = d.get('Images')
				personVideos = d.get('Videos')
				personMaps = d.get('Maps')
				personFeeds = d.get('Feeds')
				personSummary = d.get('Summary')

		print "personID:", personID
		print "personName:", personName
		print "personCrisisIDs:", personCrisisIDs
		print "personOrgIDs:", personOrgIDs
		print "personKind:", personKind
		print "personLocation:", personLocation
		print "personCitations = ", personCitations
		print "personExternalLinks = ", personExternalLinks
		print "personImages = ", personImages
		print "personVideos = ", personVideos
		print "personMaps = ", personMaps
		print "personFeeds = ", personFeeds
		print "personSummary = ", personSummary



		# Parse organizations.
		while (nextElement.tag == "Organization"):
			
			print 'nextElement.tag == "org":', nextElement.tag == "Organization"

			orgAttributes = getTextAndAttributes(nextElement)
			orgID = orgAttributes['ID']
			orgName = orgAttributes['Name']

			orgCrisisIDs = []
			orgOrgIDs = []
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
				nextElement = treeIter.next() # First Crisis in Crises sequence
				while (nextElement.tag == "Crisis"):
					orgCrisisIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
				
			if (nextElement.tag == "Organizations"):
				nextElement = treeIter.next() # First Org in Organizations sequence
				while(nextElement.tag == "Org"):
					orgOrgIDs.append(nextElement.attrib['ID'])
					nextElement = treeIter.next()
			
			if (nextElement.tag == "Kind"):
				orgKind = nextElement.text # Kind text
				nextElement = treeIter.next()
			
			if (nextElement.tag == "Location"):
				orgLocation = nextElement.text # Location text
				nextElement = treeIter.next()

			if (nextElement.tag == "History"):
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					d=getTextAndAttributes(nextElement)
					orgHistory.append(d)
					nextElement = treeIter.next()

			if (nextElement.tag == "ContactInfo"):
				nextElement = treeIter.next()
				while(nextElement.tag == "li") :
					d=getTextAndAttributes(nextElement)
					orgContactInfo.append(d)
					nextElement = treeIter.next()

			if(nextElement.tag == "Common") :
				nextElement, treeIter, d = getCommonData(nextElement, treeIter)
				orgCitations = d.get('Citations')
				orgExternalLinks = d.get('Links')
				orgImages = d.get('Images')
				orgVideos = d.get('Videos')
				orgMaps = d.get('Maps')
				orgFeeds = d.get('Feeds')
				orgSummary = d.get('Summary')

		print "orgID:", orgID
		print "orgName:", orgName
		print "orgCrisisIDs:", orgCrisisIDs
		print "orgOrgIDs:", orgOrgIDs
		print "orgKind:", orgKind
		print "orgLocation:", orgLocation
		print "orgHistory:", orgHistory
		print "orgContactInfo:", orgContactInfo

		print "orgCitations = ", orgCitations
		print "orgExternalLinks = ", orgExternalLinks
		print "orgImages = ", orgImages
		print "orgVideos = ", orgVideos
		print "orgMaps = ", orgMaps
		print "orgFeeds = ", orgFeeds
		print "orgSummary = ", orgSummary

	except StopIteration as e:
		print "StopIteration Exception"
		pass






"""
	Takes a list of Django models and saves them to a database.
"""
def modelsToDjango(models):
	pass


			
		
		
		
"""
	Parses Django models into a new XML file. 
"""
def djangoToXml():
	pass







main()
