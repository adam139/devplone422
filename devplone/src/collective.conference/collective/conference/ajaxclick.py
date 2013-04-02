
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName

from zope import event
from collective.conference.events import ClickEvent,FollowedEvent
from collective.conference.conference import IConference

class AjaxFollow(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-follow')
    grok.require('zope2.View')
        
    def render(self):
        data = self.request.form
        import pdb
        pdb.set_trace()
        id = data['questionid'].replace('_','.')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({'object_provides': IConference.__identifier__,
                                  'id': id})

        event.notify(FollowedEvent(brains[0].getObject()))

