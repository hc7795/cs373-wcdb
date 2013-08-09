from django.db import models
from django import forms
import os


class Crisis(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.TextField(null=False)
	kind = models.TextField(null=True)
	date = models.TextField(null=True)
	time = models.TextField(null=True)
	location = models.TextField(null=True)
	humanImpact = models.TextField(null=True)
	economicImpact = models.TextField(null= True)
	resourcesNeeded = models.TextField(null=True)
	waytoHelp = models.TextField(null=True)
	people = models.TextField(null=True)
	organizations = models.TextField(null=True)
	common = models.ForeignKey('Common', null=True)
	slug = models.SlugField(max_length=255, unique=True)

	def __unicode__(self):
	   return self.name  

class Person(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.TextField(null=False)
	kind = models.TextField(null=True)
	location = models.TextField(null=True)
	crises = models.TextField(null=True)
	organizations = models.TextField(null=True)
	common = models.ForeignKey('Common', null=True)
	slug = models.SlugField(max_length=255, unique=True)


	def __unicode__(self):
	   return self.name  
  
class Organization(models.Model):
	id = models.CharField(max_length=10, primary_key=True)
	name = models.TextField(null=False)
	kind = models.TextField(null=True)
	location = models.TextField(null=True)
	history = models.TextField(null=True)
	contact = models.TextField(null=True)
	crises = models.TextField(null=True)
	people = models.TextField(null=True)
	common = models.ForeignKey('Common', null=True)
	slug = models.SlugField(max_length=255, unique=True)


	def __unicode__(self):
	   return self.name  

class List(models.Model):
	href=models.TextField(null=True)
	embed=models.TextField(null=True)
	text=models.TextField(null=True)
	content=models.TextField(null=True)

	def __unicode__(self):
	   return \
	   "href: " + unicode(self.href) + \
	   ", embed: " + unicode(self.embed) + \
	   ", text: " + unicode(self.text) + \
	   ", content: " + unicode(self.content);

class Common(models.Model) :
	citations = models.ManyToManyField(List,  related_name ='Citations+', null=True)
	externalLinks = models.ManyToManyField(List,  related_name ='ExternalLinks+', null=True)
	images = models.ManyToManyField(List,  related_name ='Images+', null=True)
	videos = models.ManyToManyField(List,  related_name ='Videos+', null=True)
	maps = models.ManyToManyField(List,  related_name ='Maps+', null=True)
	feeds = models.ManyToManyField(List,  related_name ='Feeds+', null=True)
	summary = models.TextField(null=True)

	def __unicode__(self):
	   return \
	   "citations: " + unicode(self.citations.all()) + \
	   ", externalLinks: " + unicode(self.externalLinks.all()) + \
	   ", images: " + unicode(self.images.all()) + \
	   ", videos: " + unicode(self.videos.all()) + \
	   ", maps: " + unicode(self.maps.all()) + \
	   ", feeds: " + unicode(self.feeds.all()) + \
	   ", summary: " + unicode(self.summary)

class Document(models.Model):
	docfile = models.FileField(upload_to='static/')
	def filename(self):
		return os.path.basename(self.docfile.name)

	def abspath(self):
		return os.path.dirname(os.path.abspath(self.docfile.name))
