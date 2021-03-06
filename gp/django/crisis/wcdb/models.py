from django.db import models


class Crisis(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=100, null = True)
	date = models.CharField(max_length=25, null = True)
	time = models.CharField(max_length=25, null = True)
	location = models.TextField()
	humanImpact = models.TextField()
	economicImpact = models.TextField()
	resourcesNeeded = models.TextField()
	waytoHelp = models.TextField()
	people = models.TextField()
	organizations = models.TextField()
	common = models.ForeignKey('Common',null=True)

	def __unicode__(self):
	   return self.CrisisName  

class Person(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=100, null = True)
	location = models.CharField(max_length=10000, null = True)
	crises = models.TextField()
	organizations = models.TextField()
	common = models.ForeignKey('Common', null=True)

	def __unicode__(self):
	   return self.PersonName  
  
class Organization(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length = 200)
	kind = models.CharField(max_length=100, null = True)
	location = models.CharField(max_length=10000, null = True)
	history = models.CharField(max_length=1000)
	contact = models.CharField(max_length=50)
	crises = models.TextField()
	people = models.TextField()
	common = models.ForeignKey('Common', null=True)

	def __unicode__(self):
	   return self.OrganizationName  


class List(models.Model):
	href=models.TextField(null=True)
	embed=models.TextField(null=True)
	text=models.TextField(null=True)
	content=models.TextField(null=True)



class Common(models.Model) :
	citations = models.ManyToManyField(List,  related_name ='Citations+', null=True)
	externalLinks = models.ManyToManyField(List,  related_name ='ExternalLinks+', null=True)
	images = models.ManyToManyField(List,  related_name ='Images+', null=True)
	videos = models.ManyToManyField(List,  related_name ='Videos+', null=True)
	maps = models.ManyToManyField(List,  related_name ='Maps+', null=True)
	feeds = models.ManyToManyField(List,  related_name ='Feeds+', null=True)
	summary = models.TextField()




# Create your models here.
