from five import grok
from collective.conference.session import ISession
from collective.conference.conference import IConference
from Acquisition import aq_parent
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from collective.conference import MessageFactory as _
from plone.directives import form,dexterity
grok.templatedir('templates')

class SessionView(grok.View):
    grok.context(ISession)
    grok.name('view')
    grok.template('session_view')
    grok.require('zope2.View')

#    def update(self):
#        # Hide the editable-object border
#        self.request.set('disable_border', True)
        
    def roomName(self):
#        import pdb
#        pdb.set_trace()
        rooms = getattr(self.context, 'conference_rooms', [])
        if rooms:
            return ', '.join(rooms)
        return None

    def getConference(self):
        site = getSite()
        parent = aq_parent(self.context)
        while parent != site:
            if IConference.providedBy(parent):
                return parent
            parent = aq_parent(parent)
        return None
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='collective.conference',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="translate")
        return title
    
class EditConf(dexterity.EditForm):
    grok.name('sessionajaxedit')
    grok.context(ISession)    
    label = _(u'Edit session')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(ISession).select('title','description','minutes','conference_rooms')                  