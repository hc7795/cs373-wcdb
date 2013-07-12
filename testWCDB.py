#!/usr/bin/env python

"""
testWCDB.py

To test the program:
	% python testWCDB.py >& testWCDB.py.out
	% chmod ugo+x testWCDB.py
	% testWCDB.py >& testWCDB.py.out
"""


"""
Import.
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
from WorldCrisisDB import settings
setup_environ(settings)

# Django code.
from django.db import models
from WorldCrisisDB.wcdb.models import Person, Organization, Crisis

# xmlParser code.
from xmlParser import getTextAndAttributes

# Misc.
import logging
import StringIO
import unittest




# --------
# TestWCDB
# --------

class TestWCDB (unittest.TestCase):
	
	# def testXmlToModel_01(self):
	# 	raise Exception("No tests are implemented yet!")



	def testGetTextAndAttributes_01(self):
		testXML = """
			<element attribute1="a" attribute2="b" attribute3="c" attribute4="d">12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890</element>
		"""

		tree = ET.fromstring(testXML)
		it = tree.iter()
		pairs = getTextAndAttributes( it.next() )

		self.assert_(len(pairs) == 5)
		
		self.assert_( pairs["attribute1"] == "a" )
		self.assert_( pairs["attribute2"] == "b" )
		self.assert_( pairs["attribute3"] == "c" )
		self.assert_( pairs["attribute4"] == "d" )

		self.assert_( pairs["content"] == "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890" )

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass



	def testGetTextAndAttributes_02(self):
		testXML = """
			<Person ID="PER_OSAMAB" Name="Osama Bin Laden">
			<Crises>
				<Crisis ID="CRI_NINEOO" />
			</Crises>
			<Organizations>
				<Org ID="ORG_AQAEDA" />
			</Organizations>
			<Kind>Founder of al-Qaeda</Kind>
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/Osama_Bin_Laden">Wikipedia</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg" />
				</Images>
			</Common>
		</Person>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		pairs = getTextAndAttributes(e)

		self.assert_(len(pairs) == 2)

		self.assert_( pairs["ID"] == "PER_OSAMAB" )
		self.assert_( pairs["Name"] == "Osama Bin Laden" )

		# Advance iterator
		for i in range(10):
			e = it.next()

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass




print "TestWCDB.py"
unittest.main()
print "Done."
