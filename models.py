from django.db import models

# Create your models here.

"""
not sure if I'm using the ForeignKey correctly
need to figure out how to get the corresponding ID of other classes. guessing it's just read in but not sure
not sure if this correctly fits the schema, will look it up later tonight
"""


class Crisis(models.Model):
  crisisID = models.CharField(max_length = 25)
  crisisName = models.CharField(max_length = 50)
  people = models.ForeignKey(Person.personID) 
  org = models.ForeignKey(Organization.orgID)
  crisisKind = models.CharField(max_length = 25)
  crisisDate = models.DateTimeField(max_length = 25)
  crisisTime = models.CharField(max_length = 25)
  crisisLocation = models.CharField(max_length = 100)
  crisisHumanImpact = models.CharField(max_length = 100)
  crisisEconomicImpact = models.CharField(max_length = 100)
  crisisResourcesNeeded = models.CharField(max_length = 100)
  crisisWaytoHelp = models.CharField(max_length = 100)
  #Common???
  

class Person(models.Model):
  personID = models.CharField(max_length = 25)
  personName = models.CharField(max_length = 50)
  crisis = models.ForeignKey(Crisis.crisisID)
  org = models.ForeignKey(Organization.orgID)
  personKind = models.CharField(max_length = 25)
  personLocation = models.CharField(max_length = 25)
  
class Organizations(models.Model):
  orgID = models.CharField(max_length = 25)
  crisis = models.ForeignKey(Crisis.crisisID)
  people = models.ForeignKey(Person.personID)
  orgKind = models.CharField(max_length = 25)
  orgLocation = models.CharField(max_length = 25)
  orgHistory = models.CharField(max_length = 25)
  orgContact = models.CharField(max_length = 50)
  
