#!/usr/bin/env python

"""
testWCDB.py

To test the program:
    % python testWCDB.py >& testWCDB.py.out
    % chmod ugo+x testWCDB.py
    % testWCDB.py >& testWCDB.py.out
"""

# Imports.
import StringIO
import unittest

from xmlParser import xmlToModel
from minixsv import pyxsval

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET




# --------
# TestWCDB
# --------

class TestWCDB (unittest.TestCase):
    
    def testXmlToModel_01(self):
    	raise Exception("No tests are implemented yet!")
 

print "TestWCDB.py"
unittest.main()
print "Done."
