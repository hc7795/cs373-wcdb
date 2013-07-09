from django.db import models

class Locations (models.Model):
    id = models.CharField()
    li = models.CharField(xpath="/Locations/li")
    #li = models.CharField(minOccurs="1" maxOccurs="unbounded")
    
class HumanImpact(models.Model):
    id = models.CharField()
    li = models.CharField(xpath="/HumanImpact/li")
    #li = models.CharField(minOccurs="1" maxOccurs="unbounded")
    
class EconomicImpact(models.Model):
    id = models.CharField()
    li = models.CharField(xpath="/EconomicImpact/li")
    #li = models.CharField(minOccurs="1" maxOccurs="unbounded")
    
class ResourcesNeeded(models.Model):
    id = models.CharField()
    li = models.CharField(xpath="/ResourcesNeeded/li")
    #li = models.CharField(minOccurs="1" maxOccurs="unbounded")
    
class WaysToHelp(models.Model):
    id = models.CharField()
    li = models.CharField(xpath="/WaysToHelp/li")
    #li = models.CharField(minOccurs="1" maxOccurs="unbounded")
    
class Common(models.Model) :
    id = models.CharField()
    Citations = models.CharField(xpath="/Common/Citations")
    ExternalLinks = models.CharField(xpath="/Common/Citations")
    ExternalLinks = models.CharField(xpath="/Common/Citations")
    Videos = models.CharField(xpath="/Common/Citations")
    Maps = models.CharField(xpath="/Common/Citations")
    Feeds = models.CharField(xpath="/Common/Citations")
    Summary = models.CharField(xpath="/Common/Citations")
    
class Crisis(models.Model) :
    ID = models.CharField(max_length=None, primary_key=True, unique=True)
    Name = models.CharField()
    
    Kind = models.CharField(max_length=None)
    Date = models.IntField
    Time = models.IntField
    Locations = models.CharField
    
    Human_Impact = models.ForeignKey(HumanImpact)
    Economic_Impact = models.ForeignKey(EconomicImpact)
    Resources_Needed = models.ForeignKey(ResourcesNeeded)
    Ways_To_Help = models.ForeignKey(WaysToHelp)
    Common = models.ForeignKey(Common)
    
    
    
class Person(models.Model) :

class Org(models.Model) :


