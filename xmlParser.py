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
	    print "Bad file; Validation aborted!"
	    return

	except GenXmlIfError as errstr:
	    print errstr
	    print "Error; Parsing aborted!"
	    return

	# Get a list of model objects from xmlTree.
	modelsList = elementTreeToModels(xmlTree)

	# Put the models in the Django database.
	modelsToDjango(modelsList)





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
   	 # Parse crises.    
   	        while (nextElement.tag == "Crisis"):
   		        crisisAttributes = nextElement.items()
   		        crisisID = [pair[1] for pair in crisisAttributes if pair[0] == "ID"][0]
   		        crisisName = [pair[1] for pair in crisisAttributes if pair[0] == "Name"][0]

   		        # print crisisAttributes
   			print crisisID
   			print crisisName
   		 
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
   		 	crisisCommonBoolean = False # check the existence of Common
			crisisCitations = []
			crisisExternalLinks = []
			crisisImages = []
			crisisVideos = []
			crisisMaps = []
			crisisFeeds = []
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
   		 	    nextElement = treeIter.next()
			    while(nextElement.tag == "li") :
			        crisisLocations.append(nextElement.text)
				nextElement = treeIter.next()

			if(nextElement.tag == "HumanImpact") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
			        crisisHumanImpact.append(nextElement.text)
				nextElement = treeIter.next()

			if(nextElement.tag == "EconomicImpact") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
			        crisisEconomicImpact.append(nextElement.text)
				nextElement = treeIter.next()

			if(nextElement.tag == "ResourcesNeeded") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
			        crisisResourcesNeeded.append(nextElement.text)
				nextElement = treeIter.next()

			if(nextElement.tag == "WaysToHelp") :
   		 	    nextElement = treeIter.next()
   		 	    while(nextElement.tag == "li") :
			        crisisWaysToHelp.append(nextElement.text)
				nextElement = treeIter.next()

			if(nextElement.tag == "Common") :
			    crisisCommonBoolean=True
   		 	    nextElement = treeIter.next()
   		 	#    if(nextElement.tag == "Citations") :
			#	while(nextElement.tag == "li") :
			 #           crisisCommon.append(nextElement.text)
			#	    nextElement = treeIter.next()

			    if(nextElement.tag == "ExternalLinks") :
				nextElement = treeIter.next()
				while(nextElement.tag == "li"):
				    dict={}
				    ExternalAttributes = nextElement.items()
				    ExternalAttHref = [pair[1] for pair in ExternalAttributes if pair[0] == "href"][0]
				    ExternalAttEmbed = [pair[1] for pair in ExternalAttributes if pair[0] == "embed"][0]
				    ExternalAttText = [pair[1] for pair in ExternalAttributes if pair[0] == "text"][0]
				    if(ExternalAttHref != None):
					dict['href'] =ExternalAttHref
				    if(ExternalAttEmbed != None):
					dict['embed'] =ExternalAttEmbed
				    if(ExternalAttText != None):
					dict['text'] =ExternalAttText
				    crisisExternalLinks.append(dict)
				    nextElement = treeIter.next(ExternalAtt)
			        print "    honghui choi         ************  ", crisisExternalLinks

			    if(nextElement.tag == "Images") :
			        #crisisCommon.append(nextElement.text)
				while(nextElement.tag == "li") :
			            crisisCommon.append(nextElement.text)
				    nextElement = treeIter.next()
			    if(nextElement.tag == "Videos") :
			        crisisCommon.append(nextElement.text)
				while(nextElement.tag == "li") :
			            crisisCommon.append(nextElement.text)
				    nextElement = treeIter.next()
			    if(nextElement.tag == "Mapss") :
			        crisisCommon.append(nextElement.text)
				while(nextElement.tag == "li") :
			            crisisCommon.append(nextElement.text)
				    nextElement = treeIter.next()
			    if(nextElement.tag == "Feeds") :
			        crisisCommon.append(nextElement.text)
				while(nextElement.tag == "li") :
			            crisisCommon.append(nextElement.text)
				    nextElement = treeIter.next()
			    if(nextElement.tag == "Summary") :
			        crisisCommon.append(nextElement.text)
				while(nextElement.tag == "li") :
			            crisisCommon.append(nextElement.text)
				    nextElement = treeIter.next()


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
   		#print "crisisCommon = ", crisisCommon
	    
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

		print "personID:", personID
		print "personName:", personName
		print "personCrisisIDs:", personCrisisIDs
		print "personOrgIDs:", personOrgIDs
		print "personKind:", personKind
		print "personLocation:", personLocation


		# Parse organizations.
		while (nextElement.tag == "Organization"):
			
			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next()
			
			#print nextElement; print nextElement.attrib; print nextElement.text  #Crises
			nextElement = treeIter.next() #First Crisis in Crises Sequence
			while(nextElement.tag == "Crisis") :
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()
			
			#print nextElement; print nextElement.attrib; print nextElement.text #People
			nextElement = treeIter.next()
			while(nextElement.tag == "Person") :
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()
				
			#print nextElement; print nextElement.attrib; print nextElement.text #Kind Element
			nextElement = treeIter.next()
			
			#print nextElement; print nextElement.attrib; print nextElement.text #Location Element
			nextElement = treeIter.next()
			
			#print nextElement; print nextElement.attrib; print nextElement.text #History Element
			nextElement = treeIter.next() #First li in History Sequence
			while(nextElement.tag == "li") :
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()
			
			#print nextElement; print nextElement.attrib; print nextElement.text #ContactInfo
			nextElement = treeIter.next() #First li in ContactInfo Sequence
			while(nextElement.tag == "li") :
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

	except StopIteration as e:
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
