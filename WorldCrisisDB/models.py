from django.db import models

# Create your models here.
  

class Person(models.Model):
#	personID = models.AutoField(primary_key=True)
#	id = models.AutoField(primary_key=True)
#	personID = models.CharField(max_length=25)
	personID = models.CharField(primary_key=True, max_length=25)
	personName = models.CharField(max_length=50)
	personKind = models.CharField(max_length=25)
	personLocation = models.CharField(max_length=25)
#	crisis = models.ForeignKey('Crisis', related_name='person_crisis')
#	org = models.ForeignKey('Organizations', related_name='person_org')
#	com = models.ForeignKey('Common', related_name='person_com')
  
class Organizations(models.Model):
#	orgID = models.AutoField(primary_key=True)
#	id = models.AutoField(primary_key=True)
#	orgID = models.CharField(max_length=25)
	orgID = models.CharField(primary_key=True, max_length=25)
	orgname = models.CharField(max_length = 25)
	orgKind = models.CharField(max_length=25)
	orgLocation = models.CharField(max_length=25)
	orgHistory = models.CharField(max_length=25)
	orgContact = models.CharField(max_length=50)
#	crisis = models.ForeignKey('Crisis', related_name='organizations_crisis')
#	people = models.ForeignKey(Person, related_name='organizations_people')
#	com = models.ForeignKey('Organizations', related_name = 'organizations_com')

class Crisis(models.Model):
#	crisisID = models.AutoField(primary_key=True)
	crisisID = models.CharField(primary_key=True, max_length=25)
#	id = models.AutoField(primary_key=True)
#	crisisID = models.CharField(max_length=25)
	crisisName = models.CharField(max_length=50)
	crisisManager = models.Manager()
	"""
	crisisKind = models.CharField(max_length=25)
#	crisisDate = models.DateTimeField(max_length=25)
	crisisTime = models.CharField(max_length=25)
	crisisLocation = models.CharField(max_length=100)
	crisisHumanImpact = models.CharField(max_length=100)
	crisisEconomicImpact = models.CharField(max_length=100)
	crisisResourcesNeeded = models.CharField(max_length=100)
	crisisWaytoHelp = models.CharField(max_length=100)
#	people = models.ForeignKey('Person', related_name='crisis_people') 
#	org = models.ForeignKey('Organizations', related_name='crisis_org')
#	com = models.ForeignKey('Common', related_name = 'crisis_com')
	"""

"""
class Common(models.Model) :
	commonCitations = models.CharField(max_length = 100)
	commonExternalLinks = models.CharField(max_length = 100)
	commonImages = models.CharField(max_length = 100)
	commonVideos = models.CharField(max_length = 100)
	commonMaps = models.CharField(max_length = 100)
	commonFeeds = models.CharField(max_length = 100)
	commonSummary = models.CharField(max_length = 100)
"""




