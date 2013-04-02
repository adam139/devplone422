from five import grok
from Products.CMFCore.utils import getToolByName
from collective.conference.conference import IConference
from collective.conference.interfaces import IEvaluate
from collective.conference import MessageFactory as _

grok.templatedir('templates')

class ConferenceView(grok.View):
    grok.context(IConference)
    grok.name('view')
    grok.template('conference_view')
    grok.require('zope2.View')


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