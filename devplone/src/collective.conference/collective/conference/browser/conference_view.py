from five import grok
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from collective.conference.conference import IConference
from collective.conference.interfaces import IEvaluate
from collective.conference import MessageFactory as _
from Acquisition import aq_inner
from Products.CMFCore import permissions

grok.templatedir('templates')

class ConferenceView(grok.View):
    grok.context(IConference)
    grok.name('view')
    grok.template('conference_view')
    grok.require('zope2.View')

#    def update(self):
#        # Hide the editable-object border
#        self.request.set('disable_border', True)
        
    @property
    def isAnonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()
    
    @property
    def isEditable(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, 'portal_membership')
        return pm.checkPermission(permissions.ModifyPortalContent,context)  
    
    def isFollowed(self):
        obj = self.context
        aobj = IEvaluate(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)
    
    def getFollowNum(self):
        obj = self.context
        aobj = IEvaluate(obj)
        return str(aobj.followerNum)
    

    def isRegister(self):
        plists = self.context.participants
        try:
            num = len(plists)
        except:
            plists = []
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        username = userobject.getUserName()        
        return not (username in plists)  
    
    def isRegisterSpeaker(self):
        plists = self.context.speakers
        try:
            num = len(plists)
        except:
            plists = []
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        username = userobject.getUserName()        
        return not (username in plists)          