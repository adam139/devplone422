from five import grok
from collective.conference.conference import IConference
from collective.conference.participant import IParticipant
from collective.conference.session import ISession
from collective.conference.provider.listing import TableListingProvider
from plone.directives import form
from zope import schema
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from collective.conference import MessageFactory as _

grok.templatedir('templates')

class IParticipantList(IParticipant):
    form.omitted('description')

class AttendeesListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('participant-list')
    grok.require('cmf.ModifyPortalContent')

    title = _(u'Attendees listing')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize
    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        try:
            plists = list(self.context.participants)
        except:
            return TableListingProvider(self.request, IParticipantList,[])
        brains = catalog({
            'portal_type': 'dexterity.membrane.member',
            'email':plists,
            'sort_on':'sortable_title'})        
        return TableListingProvider(self.request, IParticipantList, [
            i.getObject() for i in brains
            ])


class VegetarianListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('vegetarians')
    grok.require('cmf.ModifyPortalContent')

    title = _(u'Vegetarians listing')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize        
    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        try:
            plists = list(self.context.participants)
        except:
            return TableListingProvider(self.request, IParticipantList,[])
        brains = catalog({
            'portal_type': 'dexterity.membrane.member',
            'email':plists,
            'sort_on':'sortable_title'})
        objs = [i.getObject() for i in brains] 
        return TableListingProvider(self.request, IParticipantList, [
            i for i in objs if i.is_vegetarian
        ])         
    
class ISessionList(form.Schema):

    title = schema.TextLine(
        title=_(u"Title")
    )

    session_type = schema.Choice(
        title=_(u"Session Type"),
        vocabulary="collective.conference.vocabulary.sessiontype"
    )

    level = schema.Choice(
        title=_(u"Level"),
        vocabulary="collective.conference.vocabulary.sessionlevel"
    )

    conference_rooms = schema.List(
        title=_(u"Conference Rooms"),
        value_type=schema.TextLine()
    )


class SessionListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('session-list')
    grok.require('cmf.ModifyPortalContent')

    title = _(u'Submitted Sessions')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize        
    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            }
        })
        objs = [ i.getObject() for i in brains ]
        return TableListingProvider(self.request, ISessionList, objs)


class PendingSessionListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('pending-session-list')
    grok.require('cmf.ModifyPortalContent')

    title = _(u'Pending Sessions')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize        
    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'review_state': 'pending'
        })
        objs = [ i.getObject() for i in brains ]
        return TableListingProvider(self.request, ISessionList, objs)
