
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName

from zope import event
from collective.conference.events import ClickEvent,FollowedEvent,UnfollowedEvent,RegisteredConfEvent,RegisteredSessionEvent
from collective.conference.conference import IConference

class AjaxFollow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-follow')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form

        id = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'object_provides': IConference.__identifier__,
                                  'id': id})

        event.notify(FollowedEvent(brains[0].getObject()))

class AjaxUnFollow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-unfollow')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form

        id = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'object_provides': IConference.__identifier__,
                                  'id': id})

        event.notify(UnfollowedEvent(brains[0].getObject()))

class AjaxRegConf(grok.View):
    """AJAX action: follow a question.
    """    
    grok.context(IConference)
    grok.name('ajax-register-conf')
    grok.require('zope2.View')
        
    def render(self):
        event.notify(RegisteredConfEvent(self.context))
        
class AjaxRegSession(grok.View):
    """AJAX action: follow a question.
    """    
    grok.context(IConference)
    grok.name('ajax-register-session')
    grok.require('zope2.View')
        
    def render(self):
        event.notify(RegisteredSessionEvent(self.context))        