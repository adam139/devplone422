
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent
from owasp.conference.content.conference import Iconference
from owasp.conference.content.sponsor import Isponsor

class View(grok.View):
    grok.context(Iconference)
    grok.name('view')
    grok.require('zope2.View')

#    def sessions(self):
#        """Return a catalog search result of sessions to show
#        """
#
#        context = aq_inner(self.context)
#        catalog = getToolByName(context, 'portal_catalog')
#
#        return catalog(object_provides=ISession.__identifier__,
#                       path='/'.join(context.getPhysicalPath()),
#                       sort_order='sortable_title')

class sponsorView(grok.View):
    grok.context(Isponsor)
    grok.name('view')
    grok.require('zope2.View')