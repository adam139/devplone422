#-*- coding: UTF-8 -*-
from five import grok
import json
from plone.app.layout.navigation.interfaces import INavigationRoot
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName

from zope import event
from collective.conference.events import ClickEvent,FollowedEvent,\
UnfollowedEvent,RegisteredConfEvent,UnRegisteredConfEvent,RegisteredSessionEvent
from collective.conference.conference import IConference
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p

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
#        import pdb
#        pdb.set_trace()
        mess = u"你已成功加入到 " + self.context.title
        data = {'info':mess}

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)          
#        self.request.response.redirect(self.context.absolute_url())        

class AjaxUnRegConf(grok.View):
    """AJAX action: quit a conference.
    """    
    grok.context(IConference)
    grok.name('ajax-unregister-conf')
    grok.require('zope2.View')
        
    def render(self):
        event.notify(UnRegisteredConfEvent(self.context))

        mess = u"你已成功从 " + self.context.title + u"活动中取消报名！"
        data = {'info':mess}

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
           
class AjaxRegSession(grok.View):
    """AJAX action: follow a question.
    """    
    grok.context(IConference)
    grok.name('ajax-register-session')
    grok.require('zope2.View')
        
    def render(self):
        event.notify(RegisteredSessionEvent(self.context))        