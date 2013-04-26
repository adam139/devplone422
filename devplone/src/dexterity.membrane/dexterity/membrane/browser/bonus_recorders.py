#-*- coding: UTF-8 -*-
from five import grok
import json
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName

from dexterity.membrane.content.member import IMember
from Products.CMFCore import permissions 

from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity

grok.templatedir('templates')

class bonusView(grok.View):
    grok.context(IMember)     
    grok.template('bonus_recorders')
    grok.name('bonus_recorders')
    grok.require('zope2.View')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        context = aq_inner(self.context)
        self.pm = getToolByName(context, 'portal_membership')
 
    def getMemberList(self):
        """获取会员列表"""

        userobject = self.pm.getAuthenticatedMember()
        recorders = list(userobject.getProperty('bonusrecorder'))
#        import pdb
#        pdb.set_trace()
#        recorders.reverse()
        mlist = []
        i = len(recorders)                     
        for brain in recorders:           
            row = {'id':'', 'description':''}
            row['id'] = i
            row['description'] = brain
            i = i - 1                       
            mlist.append(row)
        mlist.reverse()
        return mlist         
    
