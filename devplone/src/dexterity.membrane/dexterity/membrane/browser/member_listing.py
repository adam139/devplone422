#-*- coding: UTF-8 -*-
from five import grok
import json
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.memberfolder import IMemberfolder 
from dexterity.membrane.content.member import IMember
from Products.CMFCore import permissions 

from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity

grok.templatedir('templates')

class MemberFolderView(grok.View):
    grok.context(IMemberfolder)     
    grok.template('member_listing')
    grok.name('view')
    grok.require('cmf.ManagePortal')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
    def fullname(self):
        context = self.context
        return context.title
    
    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='dexterity.membrane',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="translate")
        return title
    
    @property
    def isEditable(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, 'portal_membership')
        return pm.checkPermission(permissions.ManagePortal,context) 

    def getMemberList(self):
        """获取申请的会议列表"""
        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog(object_provides=IMember.__identifier__, 
                                path="/".join(self.context.getPhysicalPath())
                                )

        for brain in memberbrains:
           
            row = {'id':'', 'name':'', 'url':'',
                    'email':'', 'register_date':'', 'status':'', 'editurl':'',
                    'delurl':''}
            row['id'] = brain.id
#            import pdb
#            pdb.set_trace()
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['email'] = brain.email
            row['register_date'] = brain.created.strftime('%Y-%m-%d')
            row['status'] = brain.review_state
            row['editurl'] = row['url'] + '/memberajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)

        return mlist         
class hotelstate(grok.View):
    grok.context(INavigationRoot)
    grok.name('ajaxmemberstate')
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        id = data['id']
        state = data['state']
        
        catalog = getToolByName(self.context, 'portal_catalog')
#        import pdb
#        pdb.set_trace()
        obj = catalog({'object_provides': IMember.__identifier__, "id":id})[0].getObject()        
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        if state == "disabled":
            try:
                portal_workflow.doActionFor(obj, 'enable')
                IStatusMessage(self.request).addStatusMessage(
                        _p(u'account_enabled',
                          default=u"Account:${user} has been enabled",
                          mapping={u'user': obj.title}),
                        type='info')                 
                result = True
            except:
                result = False
        else:
            try:
                portal_workflow.doActionFor(obj, 'disable')
                IStatusMessage(self.request).addStatusMessage(
                        _p(u'account_disabled',
                          default=u"Account:${user} has been disabled",
                          mapping={u'user': obj.title}),
                        type='info')                 
                result = True
            except:
                result = False
        obj.reindexObject()

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(result)     
