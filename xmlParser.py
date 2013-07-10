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


			nextElement = treeIter.next() # People element
			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First Person in People sequence
			while (nextElement.tag == "Person"):
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()


			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First Org in Organizations sequence
			while (nextElement.tag == "Org"):
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # Kind element

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # Date element

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # Time element


			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # Locations element
			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Locations sequence
			while (nextElement.tag == "li"):
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Human Impact sequence
			while (nextElement.tag == "li"): 
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Economic Impact sequence
			while (nextElement.tag == "li"): 
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in ResourcesNeeded sequence
			while (nextElement.tag == "li"): 
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in WaysToHelp sequence
			while (nextElement.tag == "li"): 
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # Citations Element

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Citations sequence
			while (nextElement.tag == "li"): 
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in External Links li
			while (nextElement.tag == "li"): # Going through External Links li
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Images li
			while (nextElement.tag == "li"): # Going through Images li
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Videos li
			while (nextElement.tag == "li"): # Going through Videos li
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Maps li
			while (nextElement.tag == "li"): # Going through Maps li
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next() # First li in Feeds li
			while (nextElement.tag == "li"): # Going through Feeds li
				#print nextElement; print nextElement.attrib; print nextElement.text
				nextElement = treeIter.next()

			#print nextElement; print nextElement.attrib; print nextElement.text
			nextElement = treeIter.next()
			#print nextElement; print nextElement.attrib; print nextElement.text

	    
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

			orgAttributes = nextElement.items()
			orgID = [pair[1] for pair in orgAttributes if pair[0] == "ID"][0]
			orgName = [pair[1] for pair in orgAttributes if pair[0] == "Name"][0]

			orgCrisisIDs = []
			orgPeopleIDs = []
			orgContactInfo = []

			nextElement = treeIter.next()

			if (nextElement.tag == "Crises"):
				nextElement = treeIter.next() # First Crisis in Crises sequence
				while (nextElement.tag == "Crisis"):
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

			print "orgID:", orgID
			print "orgName:", orgName
			print "orgCrisisIDs:", orgCrisisIDs
			print "orgPeopleIDs:", orgPeopleIDs
			print "orgKind:", orgKind
			print "orgLocation:", orgLocation
			print "orgHistory:", orgHistory

			if (nextElement.tag == "ContactInfo"):
				print "pass ContactInfo"
				nextElement = treeIter.next() 
				while (nextElement.tag == "li"):
					orgContactInfo.append(nextElement.text)
					print "orgContactInfo:", orgContactInfo
					nextElement = treeIter.next()
			


			#print "orgContactInfo:", orgContactInfo


	except StopIteration as e:
		print "StopIteration"
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
