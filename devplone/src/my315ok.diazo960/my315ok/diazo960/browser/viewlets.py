from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import LogoViewlet,SiteActionsViewlet,GlobalSectionsViewlet
from plone.app.layout.links.viewlets import FaviconViewlet
from plone.app.layout.viewlets.common import PersonalBarViewlet
from Acquisition import aq_base, aq_inner
from plone.app.layout.viewlets.common import PathBarViewlet
from Products.CMFCore.utils import getToolByName

from zope.component import getMultiAdapter


class MyLogoViewlet(LogoViewlet):
    render = ViewPageTemplateFile('templates/logo.pt')
class MyFaviconViewlet(FaviconViewlet):
    render = ViewPageTemplateFile('templates/favicon.pt') 

class GlobalSectionsViewlet(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('templates/sections.pt')


    def update(self):
        context = aq_inner(self.context)
        portal_tabs_view = getMultiAdapter((context, self.request),
                                           name='portal_tabs_view')
        self.portal_tabs = portal_tabs_view.topLevelTabs()

#        discard_tabs = ['pub','news','events','Members']
#        tp = self.portal_tabs

#        for tmp in tp:
#            if tmp["id"] in discard_tabs:                
#                self.portal_tabs.remove(tmp)        

        self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
        self.selected_portal_tab = self.selected_tabs['portal']

    def selectedTabs(self, default_tab='index_html', portal_tabs=()):
        plone_url = getToolByName(self.context, 'portal_url')()
        plone_url_len = len(plone_url)
        request = self.request
        valid_actions = []

        url = request['URL']
        path = url[plone_url_len:]

        for action in portal_tabs:
            if not action['url'].startswith(plone_url):
                # In this case the action url is an external link. Then, we
                # avoid issues (bad portal_tab selection) continuing with next
                # action.
                continue
            action_path = action['url'][plone_url_len:]
            if not action_path.startswith('/'):
                action_path = '/' + action_path
            if path.startswith(action_path + '/'):
                # Make a list of the action ids, along with the path length
                # for choosing the longest (most relevant) path.
                valid_actions.append((len(action_path), action['id']))

        # Sort by path length, the longest matching path wins
        valid_actions.sort()
        if valid_actions:
            return {'portal' : valid_actions[-1][1]}

        return {'portal' : default_tab}


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

        
  
        
        

