from django.db import models

# Create your models here.
  

class Person(models.Model):
    personID = models.CharField(max_length=25)
    personName = models.CharField(max_length=50)
    crisis = models.ForeignKey('Crisis', related_name='person_crisis')
    org = models.ForeignKey('Organizations', related_name='person_org')
    personKind = models.CharField(max_length=25)
    personLocation = models.CharField(max_length=25)
  
class Organizations(models.Model):
    orgID = models.CharField(max_length=25)
    crisis = models.ForeignKey('Crisis', related_name='organizations_crisis')
    people = models.ForeignKey(Person, related_name='organizations_people')
    orgKind = models.CharField(max_length=25)
    orgLocation = models.CharField(max_length=25)
    orgHistory = models.CharField(max_length=25)
    orgContact = models.CharField(max_length=50)
    
class Crisis(models.Model):
    crisisID = models.CharField(max_length=25)
    crisisName = models.CharField(max_length=50)
    people = models.ForeignKey('Person', related_name='crisis_people') 
    org = models.ForeignKey('Organizations', related_name='crisis_org')
    crisisKind = models.CharField(max_length=25)
    crisisDate = models.DateTimeField(max_length=25)
    crisisTime = models.CharField(max_length=25)
    crisisLocation = models.CharField(max_length=100)
    crisisHumanImpact = models.CharField(max_length=100)
    crisisEconomicImpact = models.CharField(max_length=100)
    crisisResourcesNeeded = models.CharField(max_length=100)
    crisisWaytoHelp = models.CharField(max_length=100)

class Common(models.Model)
  commonCitations = models.CharField(max_length = None)
  commonExternalLinks = models.CharField(max_length = None)
  commonImages = models.CharField(max_length = None)
  commonVideos = models.CharField(max_length = None)
  commonMaps = models.CharField(max_length = None)
  commonFeeds = models.CharField(max_length = None)
  commonSummary = models.CharField(max_length = None)




