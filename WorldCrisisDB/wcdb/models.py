from django.db import models

# Create your models here.
  

class Person(models.Model):
  ID = models.CharField(max_length=10)
  name = models.CharField(max_length=100)
#  slug = models.SlugField(max_length = 100)

  def __unicode__(self):
    return self.name 

"""
	crisis = models.ForeignKey('Crisis', related_name='person_crisis')
	organization = models.ForeignKey('Organization', related_name='person_organization')
	kind = models.CharField(max_length=100)
	location = models.CharField(max_length=200)
	
 """
class Organization(models.Model):
  ID = models.CharField(max_length=10)
  name = models.CharField(max_length=100)
#  slug = models.SlugField(max_length = 100)

  def __unicode__(self):
    return self.name

"""
	slug = models.SlugField(unique = True)
	crisis = models.ForeignKey('Crisis', related_name='organization_crisis')
	people = models.ForeignKey(Person, related_name='organization_people')
	kind = models.CharField(max_length=25)
	location = models.CharField(max_length=100)
	history = models.TextField()
	contact = models.CharField(max_length=200)

"""		
class Crisis(models.Model):
  ID = models.CharField(max_length=10)
  name = models.CharField(max_length=100)
#  slug = models.SlugField(max_length = 100)

  def __unicode__(self):
    return self.name 

"""
	slug = models.SlugField(unique = True)
	people = models.ForeignKey(Person, related_name='crisis_people') 
	organization = models.ForeignKey('Organization', related_name='crisis_organization')
	kind = models.CharField(max_length=25)
	date = models.DateTimeField(max_length=25)
	location = models.DateField()
	humanImpact = models.TextField()
	economicImpact = models.TextField()
	resourcesNeeded = models.TextField()
	waytoHelp = models.TextField()

"""
"""
class Common(models.Model):
	commonCitations = models.TextField()
	commonExternalLinks = models.TextField()
	commonImages = models.TextField()
	commonVideos = models.TextField()
	commonMaps = models.TextField()
	commonFeeds = models.TextField()
	commonSummary = models.TextField()


"""
