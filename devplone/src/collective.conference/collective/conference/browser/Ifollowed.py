#-*- coding: UTF-8 -*-
from five import grok
import json

from zope.interface import Interface
from plone.memoize.instance import memoize

from collective.conference.conference import IConference
from collective.conference.session import ISession

from zope.interface import Interface
from z3c.relationfield import RelationCatalog
from zc.relation.interfaces import ICatalog
from zope import component
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.app.layout.navigation.interfaces import INavigationRoot
from AccessControl.SecurityManagement import getSecurityManager
from plone.app.layout.globals.context import ContextState

from collective.conference.interfaces import IEvaluate

grok.templatedir('templates')


## I created conferences
class MyConferences(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')    
    grok.name('myconferences')
    grok.template('my_conferences')    
    
    def update(self):
        
#        self.haveFollower = bool(self.IFollowedNum()>0)
        self.FollowerNum = self.IFollowedNum()
        self.request.set('disable_border', True)

    @property
    def isAnonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()
    
    def IFollowedNum(self):
        """当前用户关注话题数目""" 

        if self.isAnonymous:return 0
        return len(self.IFollowedAll())
    
    @memoize    
    def IFollowedAll(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()

        username = userobject.getUserName()       

        catalog = getToolByName(self.context, 'portal_catalog')

        qbrain = catalog({'object_provides': IConference.__identifier__,
                             'Creator':username,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})   
        return qbrain         

                
    def fetchIfollowed(self, start=0, size=10):
#        import pdb
#        pdb.set_trace()
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getUserName()
        userid = userobject.getId()        
        catalog = getToolByName(self.context, 'portal_catalog')

        qbrain = catalog({'object_provides': IConference.__identifier__,
                             'Creator':username,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'b_start': start,
                             'b_size': size})
                                     
        if len(qbrain) == 0:
            qbrain = catalog({'object_provides': IConference.__identifier__,
                             'Creator':userid,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'b_start': start,
                             'b_size': size})            
    
        return qbrain         
        
class MyConferencesMore(grok.View):
    """AJAX action for updating followed conference.
    """
    
    grok.context(INavigationRoot)
    grok.name('myconferencesmore')
    grok.require('zope2.View')

    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3
                
        questionfollowed_view = getMultiAdapter((self.context, self.request),name=u"myconferences")
        questionfollowednum = questionfollowed_view.IFollowedNum()
        
        if nextstart>=questionfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = questionfollowed_view.fetchIfollowed(formstart, 3)             
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
#            questionid = braindata[i].id.replace('.','_')
                        
            out = """<div class="qbox hrbottom">
                        <div class="row-fluid">
                            <a href="%s">%s</a>
                        </div></div>"""%(questionUrl,questionTitle)
                
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,}
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
            
## I followed conferences        
class questionfollowed(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')    
    grok.name('followed')
    grok.template('Ifollowed_conferences')    
    
    def update(self):
        
#        self.haveFollower = bool(self.IFollowedNum()>0)
        self.FollowerNum = self.IFollowedNum()
        self.request.set('disable_border', True)

    @property
    def isAnonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()
    
    def IFollowedNum(self):
        """当前用户关注话题数目""" 

        if self.isAnonymous:return 0
        return len(self.IFollowedAll())
    
    @memoize    
    def IFollowedAll(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        
        questionlist = list(userobject.getProperty('myquestions'))
        catalog = getToolByName(self.context, 'portal_catalog')
        questionlist.reverse()
   
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionlist})        
        return qbrain         

                
    def fetchIfollowed(self, start=0, size=10):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getUserName()
        
        questionlist = list(userobject.getProperty('myquestions'))
        catalog = getToolByName(self.context, 'portal_catalog')        
# newest add follow sort by followed time        
        questionlist.reverse()
        startsize = start*size
        endsize = (start+1)*size
        questionGroup = questionlist[startsize:endsize]
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionGroup})        
        return qbrain       

class followedmore(grok.View):
    """AJAX action for updating followed conference.
    """
    
    grok.context(INavigationRoot)
    grok.name('followedmore')
    grok.require('zope2.View')

    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3
                
        questionfollowed_view = getMultiAdapter((self.context, self.request),name=u"followed")
        questionfollowednum = questionfollowed_view.IFollowedNum()
        
        if nextstart>=questionfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = questionfollowed_view.fetchIfollowed(formstart, 3)             
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
#            questionid = braindata[i].id.replace('.','_')
                        
            out = """<div class="qbox hrbottom">
                        <div class="row-fluid">
                            <a href="%s">%s</a>
                        </div></div>"""%(questionUrl,questionTitle)
                
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,}
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)   
    
## I have joined conference

class conferencejoined(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')    
    grok.name('conferences_joined')
    grok.template('conferences_joined')    
    
    def update(self):
        
        self.FollowerNum = self.IFollowedNum()
        self.request.set('disable_border', True)

    @property
    def isAnonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()
    
    def IFollowedNum(self):
        """当前用户关注话题数目""" 

        if self.isAnonymous:return 0
        return len(self.IFollowedAll())
    
    @memoize    
    def IFollowedAll(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        
        questionlist = list(userobject.getProperty('conferences'))
        catalog = getToolByName(self.context, 'portal_catalog')
        questionlist.reverse()
   
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionlist})        
        return qbrain         

                
    def fetchIfollowed(self, start=0, size=10):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getUserName()
        
        questionlist = list(userobject.getProperty('conferences'))
        catalog = getToolByName(self.context, 'portal_catalog')        
# newest add follow sort by followed time        
        questionlist.reverse()
        startsize = start*size
        endsize = (start+1)*size
        questionGroup = questionlist[startsize:endsize]
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionGroup})        
        return qbrain       

class conferencejoinedmore(grok.View):
    """AJAX action for updating joined conference.
    """
    
    grok.context(INavigationRoot)
    grok.name('conferences_joined_more')
    grok.require('zope2.View')

    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3
                
        questionfollowed_view = getMultiAdapter((self.context, self.request),name=u"conferences_joined")
        questionfollowednum = questionfollowed_view.IFollowedNum()
        
        if nextstart>=questionfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = questionfollowed_view.fetchIfollowed(formstart, 3)             
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
#            questionid = braindata[i].id.replace('.','_')
                        
            out = """<div class="qbox hrbottom">
                        <div class="row-fluid">
                            <a href="%s">%s</a>
                        </div></div>"""%(questionUrl,questionTitle)
                
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,}
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
## I have joined speeches

class speechjoined(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')    
    grok.name('speeches_joined')
    grok.template('speeches_joined')  
    
    def update(self):
        
#        self.haveFollower = bool(self.IFollowedNum()>0)
        self.FollowerNum = self.IFollowedNum()
        self.request.set('disable_border', True)

    @property
    def isAnonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()
    
    def IFollowedNum(self):
        """当前用户关注话题数目""" 

        if self.isAnonymous:return 0
        return len(self.IFollowedAll())
    
    @memoize    
    def IFollowedAll(self):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        
        questionlist = list(userobject.getProperty('speeches'))
        catalog = getToolByName(self.context, 'portal_catalog')
        questionlist.reverse()
   
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionlist})        
        return qbrain         

                
    def fetchIfollowed(self, start=0, size=10):
        mp = getToolByName(self.context,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getUserName()
        
        questionlist = list(userobject.getProperty('speeches'))
        catalog = getToolByName(self.context, 'portal_catalog')        
# newest add follow sort by followed time        
        questionlist.reverse()
        startsize = start*size
        endsize = (start+1)*size
        questionGroup = questionlist[startsize:endsize]
        qbrain = catalog({'object_provides': IConference.__identifier__,
                        'id':questionGroup})        
        return qbrain       

class speechjoinedmore(grok.View):
    """AJAX action for updating joined conference.
    """
    
    grok.context(INavigationRoot)
    grok.name('speeches_joined_more')
    grok.require('zope2.View')

    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")        
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) 
        nextstart = (formstart+1)*3
                
        questionfollowed_view = getMultiAdapter((self.context, self.request),name=u"speeches_joined")
        questionfollowednum = questionfollowed_view.IFollowedNum()
        
        if nextstart>=questionfollowednum :
            ifmore =  1
        else :
            ifmore = 0
        
        braindata = questionfollowed_view.fetchIfollowed(formstart, 3)             
        
        outhtml = ""
        brainnum = len(braindata)
        for i in range(brainnum):
            questionUrl = braindata[i].getURL()
            questionTitle = braindata[i].Title
#            questionid = braindata[i].id.replace('.','_')
                        
            out = """<div class="qbox hrbottom">
                        <div class="row-fluid">
                            <a href="%s">%s</a>
                        </div></div>"""%(questionUrl,questionTitle)
                
            outhtml =outhtml+out
            
        data = {                
            'outhtml': outhtml,
            'ifmore':ifmore,}
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)            