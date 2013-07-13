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
import settings
setup_environ(settings)

# Django code.
from django.db import models
from wcdb.models import Person, Organization, Crisis

# xmlParser code.
from xmlParser import getTextAndAttributes, getCommonData, elementTreeToModels, isNotDuplicate, indent

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

	def testGetTextAndAttributes_03(self):
		testXML = """
			<Crisis ID="CRI_BAGAIR" Name="Baghdad Airstrike">
			<People>
				<Person ID="PER_BRAMAN" />
				<Person ID="PER_JULASS" />
			</People>
			<Organizations>
				<Org ID="ORG_WIKLKS" />
			</Organizations>
			<Kind>War</Kind>
			<Date>2007-07-12</Date>
			<Locations>
				<li>New Baghdad, Baghdad, Iraq</li>
			</Locations>
			<HumanImpact>
				<li>12 civilians died, 2 children wounded</li>
			</HumanImpact>
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/July_12,_2007_Baghdad_airstrike">Wikipedia</li>
				</ExternalLinks>
			</Common>
		</Crisis>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		pairs = getTextAndAttributes(e)

		self.assert_(len(pairs) == 2)
		self.assert_( pairs["ID"] == "CRI_BAGAIR" )
		self.assert_( pairs["Name"] == "Baghdad Airstrike" )

		# Advance iterator
		for i in range(14):
			e = it.next()

		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_01(self):
		testXML = """
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/Iraq_war">Wikipedia</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/2/2e/Iraq_War_montage.png" />
				</Images>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["ExternalLinks"]) == 1)
		self.assert_( d["ExternalLinks"][0]["href"] == "https://en.wikipedia.org/wiki/Iraq_war" )
		self.assert_( d["Images"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/2/2e/Iraq_War_montage.png" )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_02(self):
		testXML = """
			<Common>
				<Citations>
					 <li href="http://iava.org/">Official Website</li>
					 <li  embed="http://patrickstjohn.org/images/iava-logo.jpg" />
				</Citations>
				<Images>
					<li  embed="http://patrickstjohn.org/images/iava-logo.jpg" />
				</Images>
				<Summary>
					It's an organization.
				</Summary>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["Citations"]) == 2)
		self.assert_( d["Citations"][0]["href"] == "http://iava.org/" )
		self.assert_( d["Citations"][1]["embed"] == "http://patrickstjohn.org/images/iava-logo.jpg" )
		self.assert_( d["Citations"][0]["content"] == "Official Website" )
		self.assert_( d["Images"][0]["embed"] == "http://patrickstjohn.org/images/iava-logo.jpg" )
		self.assert_( d["Summary"] == " It's an organization. " )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testgetCommonData_03(self):
		testXML = """
			<Common>
				<ExternalLinks>
					<li href="http://www.fema.gov/">Official Website</li>
					<li embed="http://www.cdc.gov/">Official Website</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Images>
				<Videos>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Videos>
				<Maps>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Maps>
				<Feeds>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" />
				</Feeds>
				<Summary>
					hello
				</Summary>
			</Common>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		it = tree.iter()
		e = it.next()
		nextElement, treeIter, d = getCommonData(e, it)
		self.assert_(len(d) == 7)
		self.assert_(len(d["ExternalLinks"]) == 2)
		self.assert_( d["ExternalLinks"][0]["href"] == "http://www.fema.gov/" )
		self.assert_( d["ExternalLinks"][1]["embed"] == "http://www.cdc.gov/" )
		self.assert_( d["Images"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" )
		self.assert_( d["Maps"][0]["embed"] == "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/FEMA_logo.svg/640px-FEMA_logo.svg.png" )
		self.assert_( d["Summary"] == " hello " )


		try:
			it.next()
			raise Exception("StopIteration exception should have been raised!")
		except StopIteration as e:
			pass

	def testGetCommonData_04(self) :
		testXML = """
			<Common>
				<Citations>
					<li href="href for Citations" />
					<li embed="embed for Citations">text inside embed</li>
				</Citations>
				<Videos>
					<li  embed="embed for Videos" />
				</Videos>
			</Common>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		treeIter = tree.iter()
		nextElement = treeIter.next()
		data = {}
		self.assert_(nextElement.tag == "Common")
		nextElement, treeIter, data = getCommonData(nextElement, treeIter)
		self.assert_(data == {'Videos': [{'embed': 'embed for Videos'}], 'Summary': [], 'Maps': [], 'Citations': [{'href': 'href for Citations'}, {'content': 'text inside embed', 'embed': 'embed for Citations'}], 'ExternalLinks': [], 'Images': [], 'Feeds': []})
		self.assert_(isinstance(data, dict))
		self.assert_(data.has_key('Videos'))
		self.assert_(data.has_key('Citations'))
		self.assert_(data.get('Citations') == [{'href': 'href for Citations'}, {'content': 'text inside embed', 'embed': 'embed for Citations'}])
		self.assert_(data.get('Citations')[0] == {'href': 'href for Citations'})
		self.assert_(data.get('Citations')[1] == {'content': 'text inside embed', 'embed': 'embed for Citations'})
		self.assert_(data.get('Videos') == [{'embed': 'embed for Videos'}])
		

		
	def testGetCommonData_05(self) :
		testXML = """
			<Common>
				<ExternalLinks>
					 <li href="https://en.wikipedia.org/wiki/Osama_Bin_Laden">Wikipedia</li>
				</ExternalLinks>
				<Images>
					<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg" />
				</Images>
			</Common>
			""" 
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		treeIter = tree.iter()
		nextElement = treeIter.next()
		data = {}
		self.assert_(nextElement.tag == "Common")
		nextElement, treeIter, data = getCommonData(nextElement, treeIter)
		self.assert_(data == {'Videos': [], 'Summary': [], 'Maps': [], 'Citations': [], 'ExternalLinks': [{'content': 'Wikipedia', 'href': 'https://en.wikipedia.org/wiki/Osama_Bin_Laden'}], 'Images': [{'embed': 'https://upload.wikimedia.org/wikipedia/commons/c/ca/Osama_bin_Laden_portrait.jpg'}], 'Feeds': []})
		self.assert_(isinstance(data.get('ExternalLinks'), list))
		self.assert_(isinstance(data.get('ExternalLinks')[0], dict))
		self.assert_(data.has_key('ExternalLinks'))
		self.assert_((data.get('ExternalLinks'))[0].get('content') == "Wikipedia")

	def testelementTreeToModels_01(self):
		testXML = """
			<WorldCrises>
				<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
					<People>
						<Person ID="PER_RENPRE" />
					</People>
					<Organizations>
						<Org ID="ORG_FEDEMA" />
					</Organizations>
					<Kind>Natural Disaster</Kind>
					<Date>2008-09-01</Date>
					<Locations>
						<li>Turks and Caicos, Bahamas, Haiti, Dominican Republic, Cuba, Florida Keys, Mississippi, Louisiana, Texas, Mississippi Valley, Ohio Valley, Great Lakes region, Eastern Canada</li>
					</Locations>
					<HumanImpact>
						<li>Fatalities: 103 direct, 92 indirect</li>
					</HumanImpact>
					<EconomicImpact>
						<li>37.5 billion (2008 USD)</li>
					</EconomicImpact>
					<Common>
						<ExternalLinks>
							 <li href="https://en.wikipedia.org/wiki/Hurricane_Ike">Wikipedia</li>
						</ExternalLinks>
						<Images>
							<li  embed="https://upload.wikimedia.org/wikipedia/commons/c/c1/Hurricane_Ike_off_the_Lesser_Antilles.jpg" />
						</Images>
					</Common>
				</Crisis>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models) == 3)
		self.assert_( models[0][0].CrisisID == "CRI_HURIKE" )
		self.assert_( models[0][0].CrisisName == "Hurricane Ike" )
		self.assert_( models[0][0].crisisKind == "Natural Disaster" )
		self.assert_( models[0][0].crisisDate == "2008-09-01" )

	def testelementTreeToModels_02(self):
		testXML = """
			<WorldCrises>
				<Person ID="PER_GHARTL" Name="Gregory Hartl">
					<Crises>
						<Crisis ID="CRI_SWNFLU" />
					</Crises>
					<Organizations>
						<Org ID="ORG_WHLORG" />
					</Organizations>
					<Kind>Head of Public Relations/Social Media for World Health Organization</Kind>
					<Common>
						<ExternalLinks>
							 <li href="https://twitter.com/HaertlG">Twitter</li>
						</ExternalLinks>
						<Images>
							<li  embed="http://news.bbcimg.co.uk/media/images/67578000/jpg/_67578538_67578537.jpg" />
						</Images>
					</Common>
				</Person>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models[0]) == 0)
		self.assert_( models[1][0].PersonID == "PER_GHARTL" )
		self.assert_( models[1][0].PersonName == "Gregory Hartl" )
		self.assert_( models[1][0].personKind == "Head of Public Relations/Social Media for World Health Organization" )

	def testelementTreeToModels_03(self):
		testXML = """
			<WorldCrises>
				<Organization ID="ORG_UNICEF" Name="UNICEF">
					<Crises>
						<Crisis ID="CRI_WSAFRC" />
						<Crisis ID="CRI_HAITIE" />
					</Crises>
					<Kind>Humanitarian</Kind>
					<Location>New York, USA</Location>
					<History>
						<li>Founded in 1946</li>
					</History>
					<ContactInfo>
						<li>Phone: 1-800-FOR-KIDS</li>
					</ContactInfo>
					<Common>
						<ExternalLinks>
							 <li href="http://www.unicefusa.org/">Official Website</li>
						</ExternalLinks>
						<Images>
							<li  embed="https://upload.wikimedia.org/wikipedia/commons/d/d1/Flag_of_UNICEF.svg" />
						</Images>
					</Common>
				</Organization>
			</WorldCrises>
		"""

		# Remove tabs and newlines from testXML
		testXML = " ".join(testXML.split())

		tree = ET.fromstring(testXML)
		dictionary={};
		models = elementTreeToModels(tree,dictionary)
		self.assert_(len(models[1]) == 0)
		self.assert_( models[2][0].OrganizationID == "ORG_UNICEF" )
		self.assert_( models[2][0].OrganizationName == "UNICEF" )
		self.assert_( models[2][0].orgKind == "Humanitarian" )

	def testisNotDuplicate_01(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("d","a",dictionary)
		self.assert_(b == True)

	def testisNotDuplicate_02(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("a","a",dictionary)
		self.assert_(b == False)

	def testisNotDuplicate_03(self):
		dictionary={1:"a",2:"b",3:"c"};
		b = isNotDuplicate("c","a",dictionary)
		self.assert_(b == False)


	def test_indent_01 (self) :
		testXML = """
			<WorldCrises>
			<Crisis ID="CRI_HURIKE" Name="Hurricane Ike">
			<Kind>Natural Disaster</Kind>
			<Date>2008-09-01</Date>
			</Crisis>
			</WorldCrises>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		#ans = '<WorldCrises>\n  <Crisis ID="CRI_HURIKE" Name="Hurricane Ike"\n    <Kind>Natural Disaster</Kind>\n    <Date>2008-09-01</Date>\n  </Crisis>\n</WorldCrises>'
		self.assert_(indentReturned != testXML)		

	def test_indent_02 (self) :
		testXML = """
			<Organization ID="ORG_CARERA" Name="Care">
			<Crises>
			<Crisis ID="CRI_WSAFRC" />
			</Crises>
			</Organization>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		#ans = '<Organization ID="ORG_CARERA" Name="Care">\n  <Crises>\n    <Crisis ID="CRI_WSAFRC" />\n  </Crises>\n</Organization>'
		self.assert_(indentReturned != testXML)
		
	def test_indent_03 (self) :
		testXML = """
			<Person ID="PER_BUSDAD" Name="George H. W. Bush">
			<Crises>
			<Crisis ID="CRI_EXXONV" />
			</Crises>
			<Kind>President of the United States</Kind>
			<Common>
			<ExternalLinks>
			<li href="https://en.wikipedia.org/wiki/George_H._W._Bush">Wikipedia</li>
			</ExternalLinks>
			<Images>
			<li embed="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/George_H._W._Bush%2C_President_of_the_United_States%2C_1989_official_portrait.jpg/520px-George_H._W._Bush%2C_President_of_the_United_States%2C_1989_official_portrait.jpg" />
			</Images>
			</Common>
			</Person>
			"""
		testXML = " ".join(testXML.split())
		tree = ET.fromstring(testXML)
		indent(tree)
		indentReturned = ET.tostring(tree)
		self.assert_(indentReturned != testXML)



print "TestWCDB.py"
unittest.main()
print "Done."
