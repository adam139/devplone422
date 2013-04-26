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
    grok.name('admin_view')
    grok.require('cmf.ManagePortal')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        context = aq_inner(self.context)
        self.pm = getToolByName(context, 'portal_membership')
        
    
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
        return self.pm.checkPermission(permissions.ManagePortal,context) 

    def _getUserData(self,userId):

        member = self.pm.getMemberById(userId)
        try:
            groups = member.getGroups()
        except:
            return ""
        roles = [role for role in member.getRoles() if role != 'Authenticated']
        roles = ','.join(roles)
        return roles
        
    def getMemberList(self):
        """获取会员列表"""
        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog(object_provides=IMember.__identifier__, 
                                path="/".join(self.context.getPhysicalPath()),
                                              sort_order="reverse",
                                              sort_on="created")
                    

        for brain in memberbrains:
           
            row = {'id':'', 'name':'', 'url':'','roles':'',
                    'email':'', 'register_date':'', 'status':'', 'editurl':'',
                    'delurl':''}
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            email = brain.email
            row['roles'] = self._getUserData(email)
            row['email'] = email
            row['register_date'] = brain.created.strftime('%Y-%m-%d')
            row['status'] = brain.review_state
            row['editurl'] = row['url'] + '/memberajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist         
class memberstate(grok.View):
    grok.context(INavigationRoot)
    grok.name('ajaxmemberstate')
    grok.require('zope2.View')
    
    def render(self):
        data = self.request.form
        id = data['id']
        state = data['state']
        
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = catalog({'object_provides': IMember.__identifier__, "id":id})[0].getObject()        
        portal_workflow = getToolByName(self.context, 'portal_workflow')
# obj current status        
        if state == "disabled":
            try:
                portal_workflow.doActionFor(obj, 'enable')

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
                portal_workflow.doActionFor(obj, 'disable')
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
