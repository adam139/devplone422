from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from five import grok
from Products.CMFCore.utils import getToolByName

from my315ok.socialorgnization import _

class RegistrySource(object):
    grok.implements(IContextSourceBinder)
    
    def __init__(self,key):
        self.key = key
    
    def __call__(self,context):
        registry = queryUtility(IRegistry)
        terms = []
        vdict = registry.get(self.key,{})
        vkeys = sorted(vdict.keys())
        if registry is not None:
               for index in vkeys: 
                   value = vdict.get(index)
                   terms.append(SimpleVocabulary.createTerm(index,value,_(value)))
        return SimpleVocabulary(terms)
    
    def getKeys(self):
        registry = queryUtility(IRegistry)
        return sorted(registry.get(self.key,{}).keys())
    
    def getDict(self):
        registry = queryUtility(IRegistry)
        d = registry.get(self.key,{})
        for k in d:
            d[k] = _(d[k])
        return d
    
    def getValue(self,num):
        registry = queryUtility(IRegistry)
        if registry is not None:
            return  _(registry.get(self.key,{}).get(num))

class DynamicVocabulary(object):
    grok.implements(IContextSourceBinder)
    
    def __init__(self,key,mo,name="title"):
        self.key = key
        self.mo = mo
        self.name = name
        self.query = {}
        if self.mo == "Iarea":
            self.query = {"areastate":1}
        
    def __call__(self,context):
        terms = []
        exec("from %s import %s as mo"%(self.key,self.mo))
        catalog = getToolByName(context,"portal_catalog")
        if mo:
            self.query.update({"object_provides":mo.__identifier__})
            all = catalog(self.query)
            for s in all:
                title = s.Title
                id = s.id
                terms.append(SimpleVocabulary.createTerm(id,id,title))
        return SimpleVocabulary(terms)

class DynamicVocabularyIarea(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        from eisoo.operation.area import Iarea
        terms = []
        catalog = getToolByName(context,"portal_catalog")
        all = []
        if hasattr(context,'name') and context.name:
            areaid = context.name
            area = catalog(object_provides=Iarea.__identifier__,id=areaid)
            if area:
                level = (area[0].getObject().level,"%s"%(int(area[0].getObject().level)+1))
                all = catalog(object_provides=Iarea.__identifier__,level=level,areastate=1)
        else:
            level = "1"
            all = catalog(object_provides=Iarea.__identifier__,level=level,areastate=1)
        for s in all:
            terms.append(SimpleVocabulary.createTerm(s.id,s.id,_(s.getObject().name)))
        return SimpleVocabulary(terms)

class DynamicVocabularyIareamanaged(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context):
        from eisoo.operation.areamanaged import Iareamanaged
        terms = []
        catalog = getToolByName(context,"portal_catalog")
        tharea = catalog(id=getattr(context,"name","0"))
        if tharea:
            newlevel = tharea[0].getObject().level
        else:
            newlevel = "1"
        parea = catalog(object_provides=Iareamanaged.__identifier__)
        for s in parea:
            areamanaged = catalog(id=s.getObject().name)
            if areamanaged and areamanaged[0].getObject().level in (newlevel,str(int(newlevel)-1)):
               name = areamanaged[0].getObject().name
               terms.append(SimpleVocabulary.createTerm(s.id,s.id,_(name)))
        return SimpleVocabulary(terms)