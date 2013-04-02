from Products.CMFCore.utils import getToolByName
from zope.site.hooks import getSite
import random
from Acquisition import aq_inner, aq_base

filter = ("eisoo.topic.questionfolder","eisoo.topic.topicfolder")

def chooseName(self,name,object):
    catalog = getToolByName(getSite(),"portal_catalog")
    portal_type = aq_base(object).portal_type
    classname = portal_type.split(".")[-1]
    if classname in filter:
        return getName(self,name,object)
    if classname.find('folder',0) == -1:
        randomnum = random.randint(100000,999999)
        length   = len(catalog(portal_type=portal_type)) +1
        id = "%s%s%s"%(classname,randomnum,length)
    else:
        length = len(catalog(portal_type=portal_type)) + 1
        if length==1:
            id = classname
        else:
            id = "%s%s"%(classname,length)
    return id

def getName(self,name,object):
    container = aq_inner(self.context)
    if not name:
        nameFromTitle = INameFromTitle(object, None)
        if nameFromTitle is not None:
            name = nameFromTitle.title
        if not name:
            name = getattr(aq_base(object), 'id', None)
        if not name:
            name = getattr(aq_base(object), 'portal_type', None)
        if not name:
            name = object.__class__.__name__

    if not isinstance(name, unicode):
        name = unicode(name, 'utf-8')

    request = getattr(object.__of__(container), 'REQUEST', None)
    if request is not None:
        name = IUserPreferredURLNormalizer(request).normalize(name)
    else:
        name = getUtility(IURLNormalizer).normalize(name)
        
    return self._findUniqueName(name, object)