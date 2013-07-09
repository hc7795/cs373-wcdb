from google.appengine.ext import db

class Locations (db.Model):
    li = db.StringProperty()
    
class HumanImpact(db.Model):
    li = db.StringProperty()
    crisis = db.ReferenceProperty(Crisis, collection_name = 'waysToHelp')
    
class EconomicImpact(db.Model):
    li = db.StringProperty()
    crisis = db.ReferenceProperty(Crisis, collection_name = 'EconomicImpact')
    
class ResourcesNeeded(db.Model):
    li = db.StringProperty()
    crisis = db.ReferenceProperty(Crisis, collection_name = 'ResourcesNeeded')
    
class WaysToHelp(db.Model):
    li = db.StringProperty()
    crisis = db.ReferenceProperty(Crisis, collection_name = 'WaysToHelp')
    
class Common(db.Model) :
    Citations = db.StringProperty()
    ExternalLinks = db.StringProperty()
    ExternalLinks = db.StringProperty()
    Videos = db.StringProperty()
    Maps = db.StringProperty()
    Feeds = db.StringProperty()
    Summary = db.StringProperty()
    crisis = db.ReferenceProperty(Crisis, collection_name = 'Common')
    
class Crisis(db.Model) :
    ID = db.StringProperty()
    Name = db.StringProperty()
    
    Kind = db.StringProperty()
    Date = db.StringProperty()
    Time = db.StringProperty()
    Locations = db.StringProperty()
    
    #Human_Impact
    #Economic_Impact 
    #Resources_Needed 
    #Ways_To_Help 
    #Common
    
    
    
class Person(models.Model) :

class Org(models.Model) :


