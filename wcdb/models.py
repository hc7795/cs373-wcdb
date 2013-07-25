from django.db import models



class Crisis(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=100, null = True)
	date = models.CharField(max_length=25, null = True)
	time = models.CharField(max_length=25, null = True)
	location = models.TextField(null = True)
	humanImpact = models.TextField(null = True)
	economicImpact = models.TextField(null = True)
	resourcesNeeded = models.TextField(null = True)
	waytoHelp = models.TextField(null = True)
	people = models.TextField(null = True)
	organizations = models.TextField(null = True)
	common = models.ForeignKey('Common',null=True)
	slug = models.SlugField(max_length = 100, unique=True)

	def __unicode__(self):
	   return self.name  

class Person(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=100)
	kind = models.CharField(max_length=100, null = True)
	location = models.CharField(max_length=10000, null = True)
	crises = models.TextField(null = True)
	organizations = models.TextField(null = True)
	common = models.ForeignKey('Common', null=True)
	slug = models.SlugField(max_length = 100, unique=True)


	def __unicode__(self):
	   return self.name  
  
class Organization(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length = 200)
	kind = models.CharField(max_length=100, null = True)
	location = models.CharField(max_length=10000, null = True)
	history = models.CharField(max_length=1000)
	contact = models.CharField(max_length=50)
	crises = models.TextField(null = True)
	people = models.TextField(null = True)
	common = models.ForeignKey('Common', null=True)
	slug = models.SlugField(max_length = 100, unique=True)


	def __unicode__(self):
	   return self.name  

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
	summary = models.TextField(null=True)

