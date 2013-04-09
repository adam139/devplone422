from five import grok
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from collective.conference import MessageFactory as _
grok.templatedir('templates')

class SessionListView(grok.View):
    grok.context(IConference)
    grok.template('session_listing')
    grok.name('sessions')

    title = _(u"Sessions")

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    @memoize            
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'sortable_title'
        })
        objs = [i.getObject() for i in brains]
        return [i for i in objs if (i.session_type != 'Meta')]
