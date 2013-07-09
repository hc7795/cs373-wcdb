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


			nextElement = treeIter.next() # People element
			print nextElement
			nextElement = treeIter.next() # First Person in People sequence
			while (nextElement.tag == "Person"):
				print nextElement
				nextElement = treeIter.next()


			print nextElement
			nextElement = treeIter.next() # First Org in Organizations sequence
			while (nextElement.tag == "Org"):
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # Kind element

			print nextElement
			nextElement = treeIter.next() # Date element

			print nextElement
			nextElement = treeIter.next() # Time element


			print nextElement
			nextElement = treeIter.next() # Locations element
			print nextElement
			nextElement = treeIter.next() # First li in Locations sequence
			while (nextElement.tag == "li"):
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Human Impact sequence
			while (nextElement.tag == "li"): 
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Economic Impact sequence
			while (nextElement.tag == "li"): 
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in ResourcesNeeded sequence
			while (nextElement.tag == "li"): 
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in WaysToHelp sequence
			while (nextElement.tag == "li"): 
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # Citations Element

			print nextElement
			nextElement = treeIter.next() # First li in Citations sequence
			while (nextElement.tag == "li"): 
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in External Links li
			while (nextElement.tag == "li"): # Going through External Links li
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Images li
			while (nextElement.tag == "li"): # Going through Images li
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Videos li
			while (nextElement.tag == "li"): # Going through Videos li
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Maps li
			while (nextElement.tag == "li"): # Going through Maps li
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next() # First li in Feeds li
			while (nextElement.tag == "li"): # Going through Feeds li
				print nextElement
				nextElement = treeIter.next()

			print nextElement
			nextElement = treeIter.next()
			print nextElement

	    
		# Parse people.	
		while (nextElement.tag == "Person"):
		
			nextElement = treeIter.next() #Crises Element
			print nextElement
			nextElement = treeIter.next() #First Crisis in Crises Sequence
			while(nextElement.tag == "Crisis") :
				print nextElement
				nextElement = treeIter.next()
				
			print nextElement
			nextElement = treeIter.next()
			while(nextElement.tag == "Org") :
			    print nextElement
			    nextElement = treeIter.next()
			
			print nextElement #Kind Element
			nextElement = treeIter.next() 
			
			print nextElement # Location Element
			nextElement = treeIter.next()


		# Parse organizations.
		while (nextElement.tag == "Organization"):
			
			print nextElement
			nextElement = treeIter.next()
			
			print nextElement  #Crises
			nextElement = treeIter.next() #First Crisis in Crises Sequence
			while(nextElement.tag == "Crisis") :
				print nextElement
				nextElement = treeIter.next()
			
			print nextElement #People
			nextElement = treeIter.next()
			while(nextElement.tag == "Person") :
				print nextElement
				nextElement = treeIter.next()
				
			print nextElement #Kind Element
			nextElement = treeIter.next()
			
			print nextElement #Location Element
			nextElement = treeIter.next()
			
			print nextElement #History Element
			nextElement = treeIter.next() #First li in History Sequence
			while(nextElement.tag == "li") :
				print nextElement
				nextElement = treeIter.next()
			
			print nextElement #ContactInfo
			nextElement = treeIter.next() #First li in ContactInfo Sequence
			while(nextElement.tag == "li") :
				print nextElement
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
