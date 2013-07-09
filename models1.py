from django.db import models

# Create your models here.

"""
not sure if I'm using the ForeignKey correctly
need to figure out how to get the corresponding ID of other classes. guessing it's just read in but not sure
not sure if this correctly fits the schema, will look it up later tonight
"""


class Crisis(models.Model):
  ID = models.CharField(max_length = None)
  Name = models.CharField(max_length = None)

  crisisKind = models.CharField(max_length = None)
  crisisDate = models.DateTimeField(max_length = None)
  crisisTime = models.CharField(max_length = None)
  crisisLocation = models.CharField(max_length = None)
  crisisHumanImpact = models.CharField(max_length = None)
  crisisEconomicImpact = models.CharField(max_length = None)
  crisisResourcesNeeded = models.CharField(max_length = None)
  crisisWaytoHelp = models.CharField(max_length = None)

  people = models.ForeignKey(Person) 
  org = models.ForeignKey(Organization)

  #Common???
  

class Person(models.Model):
  ID = models.CharField(max_length = None)
  Name = models.CharField(max_length = None)
  personKind = models.CharField(max_length = None)
  personLocation = models.CharField(max_length = None)

  crisis = models.ForeignKey(Crisis)
  org = models.ForeignKey(Organization)  
  
class Organization(models.Model):
  ID = models.CharField(max_length = None)
  Name = models.CharField(max_length = None)
  orgKind = models.CharField(max_length = None)
  orgLocation = models.CharField(max_length = None)
  orgHistory = models.CharField(max_length = None)
  orgContact = models.CharField(max_length = None)

  crisis = models.ForeignKey(Crisis)
  people = models.ForeignKey(Person)

class Common(models.Model)
  commonCitations = models.CharField(max_length = None)
  commonExternalLinks = models.CharField(max_length = None)
  commonImages = models.CharField(max_length = None)
  commonVideos = models.CharField(max_length = None)
  commonMaps = models.CharField(max_length = None)
  commonFeeds = models.CharField(max_length = None)
  commonSummary = models.CharField(max_length = None)
