#!/usr/bin/env python

"""
xmlParser.py

Contains functions to parse crisis XML files into Django models and vice versa.
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from minixsv import pyxsval



def main():
	try:
		xmlToModel()

	except Exception as e:
		print "Fatal error, ending program. Error message:"
		print e





"""
Parses a XML file into Django models and saves them to the database. 
"""
def xmlToModel():

	# Uncomment the following lines when hardcoded XML/Schema files are no longer necessary.
	# xmlFilename = raw_input("Filename of the XML file: ")
	# schemaFilename = raw_input("Filename of the schema file: ")
	xmlFilename = "test/example.xml"
	schemaFilename = "test/schema.xml"

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
	    return
	   
	except GenXmlIfError as errstr:
	    print errstr
	    print "Parsing aborted!"
	    return

	treeIter = xmlTree.iter()
	nextElement = treeIter.next() # Retrieves root element
	print nextElement
	nextElement = treeIter.next() # Retrieves next Crisis element
	print nextElement

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
		nextElement = treeIter.next() #Crises
		print nextElement
		nextElement = treeIter.next()
		while(nextElement.tag == "Crisis") :
			print nextElement
			nextElement = treeIter.next()
		print nextElement
		while(nextElement.tag == "Org") :
		    print nextElement
		    nextElement = treeIter.next()
		    
	# Parse organizations.
	while (nextElement.tag == "Organization"):
		print nextElement
		nextElement = treeIter.next()


"""
Parses Django models into a new XML file. 
"""
def modelToXml():
	pass







main()