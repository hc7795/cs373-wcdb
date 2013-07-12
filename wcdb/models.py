from django.db import models


class Crisis(models.Model):
	CrisisID = models.CharField(max_length=10, primary_key=True)
	CrisisName = models.CharField(max_length=100)
	crisisKind = models.CharField(max_length=100, null = True)
	crisisDate = models.DateTimeField(max_length=25, null = True)
	crisisTime = models.CharField(max_length=25, null = True)
	crisisLocation = models.CharField(max_length=10000, null = True)
	#crisisHumanImpact = models.CharField(max_length=100)
	#crisisEconomicImpact = models.CharField(max_length=100)
	#crisisResourcesNeeded = models.CharField(max_length=100)
	#crisisWaytoHelp = models.CharField(max_length=100)
	#people = models.ForeignKey('Person', related_name='crisis_people') 
	#org = models.ForeignKey('Organizations', related_name='crisis_org')
	#com = models.ForeignKey('Common', related_name = 'crisis_com')

	def __unicode__(self):
	   return self.CrisisName  

class Person(models.Model):
	PersonID = models.CharField(max_length=10, primary_key=True)
	PersonName = models.CharField(max_length=100)
	personKind = models.CharField(max_length=100, null = True)
	personLocation = models.CharField(max_length=10000, null = True)
	#crisis = models.ForeignKey('Crisis', related_name='person_crisis')
	#org = models.ForeignKey('Organizations', related_name='person_org')
	#com = models.ForeignKey('Common', related_name='person_com')

	def __unicode__(self):
	   return self.PersonName  
  
class Organization(models.Model):
	OrganizationID = models.CharField(max_length=10, primary_key=True)
	OrganizationName = models.CharField(max_length = 200)
	orgKind = models.CharField(max_length=100, null = True)
	orgLocation = models.CharField(max_length=10000, null = True)
	#orgHistory = models.CharField(max_length=25)
	#orgContact = models.CharField(max_length=50)
	#crisis = models.ForeignKey('Crisis', related_name='organizations_crisis')
	#people = models.ForeignKey(Person, related_name='organizations_people')
	#com = models.ForeignKey('Organizations', related_name = 'organizations_com')

	def __unicode__(self):
	   return self.OrganizationName  



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




