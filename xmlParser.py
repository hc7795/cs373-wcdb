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
	xmlFilename = raw_input("Filename of the XML file: ")
	schemaFilename = raw_input("Filename of the schema file: ")

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
	   
	except GenXmlIfError as errstr:
	    print errstr
	    print "Parsing aborted!"


	treeIter = xmlTree.iter()
	nextElement = treeIter.next() # Retrieves root element
	nextElement = treeIter.next() # Retrieves next Crisis element

	# Parse crises.	
	while (nextElement.tag == "Crisis"):
		print nextElement
		peopleElement = treeIter.next()

		nextElement = treeIter.next()

		while (nextElement.tag == "Person"):
			print nextElement
			nextElement = treeIter.next()

		nextElement = treeIter.next()

	# Parse people.
	# if (nextElement.tag != "Person"): raise IOError("Expected 'Person' tag; found '" + nextElement.tag + "'!")
		
	while (nextElement.tag == "Person"):
		print nextElement
		nextElement = treeIter.next()


	# Parse organizations.
	# if (nextElement.tag != "Organization"): raise IOError("Expected 'Organization' tag; found '" + nextElement.tag + "'!")
		
	while (nextElement.tag == "Organization"):
		print nextElement
		nextElement = treeIter.next()


"""
Parses Django models into a new XML file. 
"""
def modelToXml():
	pass







main()