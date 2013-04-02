from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import LogoViewlet,SiteActionsViewlet,GlobalSectionsViewlet
from plone.app.layout.links.viewlets import FaviconViewlet
from plone.app.layout.viewlets.common import PersonalBarViewlet
from plone.app.layout.viewlets.common import PathBarViewlet

from zope.component import getMultiAdapter


class MyLogoViewlet(LogoViewlet):
    render = ViewPageTemplateFile('templates/logo.pt')
class MyFaviconViewlet(FaviconViewlet):
    render = ViewPageTemplateFile('templates/favicon.pt') 

class GlobalSectionsViewlet(GlobalSectionsViewlet):
    render = ViewPageTemplateFile('templates/sections.pt')

#    def update(self):
#        context_state = getMultiAdapter((self.context, self.request),
#                                        name=u'plone_context_state')
#        actions = context_state.actions()
#        portal_tabs_view = getMultiAdapter((self.context, self.request),
#                                           name='portal_tabs_view')
#        self.portal_tabs = portal_tabs_view.topLevelTabs(actions=actions)
#        for tmp in self.portal_tabs:
#            if tmp["id"] == "pub":
#                self.portal_tabs.remove(tmp)
#                break           
#        selectedTabs = self.context.restrictedTraverse('selectedTabs')
#        self.selected_tabs = selectedTabs('HOME',
#                                          self.context,
#                                          self.portal_tabs)
#        self.selected_portal_tab = self.selected_tabs['portal']

class SiteActionsViewlet(SiteActionsViewlet):
    render = ViewPageTemplateFile('templates/site_actions.pt')

#    def update(self):
#        context_state = getMultiAdapter((self.context, self.request),
#                                        name=u'plone_context_state')
#        self.site_actions = context_state.actions().get('site_actions', None)
        
class PersonalViewlet(PersonalBarViewlet):
    render = ViewPageTemplateFile('templates/personal.pt')


class PathBarViewlet(PathBarViewlet):

    render = ViewPageTemplateFile('templates/pathbar.pt')

        
  
        
        

