from five import grok
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from collective.conference import MessageFactory as _

grok.templatedir('templates')

class ParticipantListView(grok.View):
    grok.context(IConference)
    grok.template('profile_listing')
    grok.name('participants')
    grok.require('zope2.View')

    title = _(u"Participants")
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        

    @memoize    
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        try:
            plists = list(self.context.participants)
        except:
            return []
        brains = catalog({
            'portal_type': 'dexterity.membrane.member',
            'email':plists,
            'sort_on':'sortable_title'})
        return [i.getObject() for i in brains]    
