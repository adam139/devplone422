#-*- coding: UTF-8 -*-
from five import grok
from collective.conference.conference import IConference
from collective.conference.session import ISession
from plone.app.layout.navigation.interfaces import INavigationRoot
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

class Sessions_adminView(grok.View):
    grok.context(INavigationRoot)
    grok.template('session_listing_admin')
    grok.name('sessions_admin')
    grok.require('cmf.ManagePortal')    
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
    
    @property
    def isEditable(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, 'portal_membership')
        return pm.checkPermission(permissions.ManagePortal,context) 

    def getSessionList(self):
        """获取申请的会议列表"""
        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog({'object_provides':ISession.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                                             
                                              )


        for brain in memberbrains:
           
            row = {'id':'', 'name':'', 'url':'',
                    'conference_rooms':'', 'conference_created':'','status':'','editurl':'',
                    'delurl':''}
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['conference_rooms'] = brain.conference_rooms
            row['session_created'] = brain.created.strftime('%Y-%m-%d')
            row['status'] = brain.review_state
#            import pdb
#            pdb.set_trace()
            row['editurl'] = row['url'] + '/sessionajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist         
class Sessionstate(grok.View):
    grok.context(INavigationRoot)
    grok.name('ajaxsessionstate')
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        id = data['id']
        state = data['state']
        
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = catalog({'object_provides': ISession.__identifier__, "id":id})[0].getObject()        
        portal_workflow = getToolByName(self.context, 'portal_workflow')
# obj current status        
        if state == "pending":
            try:
                portal_workflow.doActionFor(obj, 'accept')
                portal_workflow.doActionFor(obj, 'publish')                

                result = True
#                IStatusMessage(self.request).addStatusMessage(
#                        _p(u'account_enabled',
#                          default=u"Account:${user} has been enabled",
#                          mapping={u'user': obj.title}),
#                        type='info')                 

            except:
                result = False
        else:
            try:
                portal_workflow.doActionFor(obj, 'retract')
                result = True                
#                IStatusMessage(self.request).addStatusMessage(
#                        _p(u'account_disabled',
#                          default=u"Account:${user} has been disabled",
#                          mapping={u'user': obj.title}),
#                        type='info')                 

            except:
                result = False
        obj.reindexObject()

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(result)   