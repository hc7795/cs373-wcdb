from django.db import models
#from django_orm.postgresql.fields.arrays import ArrayField
# Create your models here.
#from django_orm.manager import Manager

class Person(models.Model):
	personID = models.CharField(max_length=10)
	personName = models.CharField(max_length=100)
	#personKind = models.CharField(max_length=25)
	#personLocation = models.CharField(max_length=25)
	#crisis = models.ForeignKey('Crisis', related_name='person_crisis')
	#org = models.ForeignKey('Organizations', related_name='person_org')
	#com = models.ForeignKey('Common', related_name='person_com')
  
class Organization(models.Model):
	orgID = models.CharField(max_length=10)
	orgName = models.CharField(max_length = 200)
	#orgKind = models.CharField(max_length=25)
	#orgLocation = models.CharField(max_length=25)
	#orgHistory = models.CharField(max_length=25)
	#orgContact = models.CharField(max_length=50)
	#crisis = models.ForeignKey('Crisis', related_name='organizations_crisis')
	#people = models.ForeignKey(Person, related_name='organizations_people')
	#com = models.ForeignKey('Organizations', related_name = 'organizations_com')

class Crisis(models.Model):
	crisisID = models.CharField(max_length=10)
	crisisName = models.CharField(max_length=100)
	#crisisKind = models.CharField(max_length=25)
	#crisisDate = models.DateTimeField(max_length=25)
	#crisisTime = models.CharField(max_length=25)
	#crisisLocation = models.CharField(max_length=100)
	#crisisHumanImpact = models.CharField(max_length=100)
	#crisisEconomicImpact = models.CharField(max_length=100)
	#crisisResourcesNeeded = models.CharField(max_length=100)
	#crisisWaytoHelp = models.CharField(max_length=100)
	#people = models.ForeignKey('Person', related_name='crisis_people') 
	#org = models.ForeignKey('Organizations', related_name='crisis_org')
	#com = models.ForeignKey('Common', related_name = 'crisis_com')

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




