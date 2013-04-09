from five import grok
from Acquisition import aq_inner
from zope.component import getMultiAdapter

from plone.directives import form
from zope import schema
from z3c.form import form, field
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.content.member import IMember 

from dexterity.membrane.behavior.membraneuser import IProvidePasswords 
from plone.app.layout.navigation.interfaces import INavigationRoot
from dexterity.membrane import _
from plone.directives import dexterity

grok.templatedir('templates')

class MembraneMemberView(grok.View):
    grok.context(IMember)     
    grok.template('member_view')
    grok.name('view')
    grok.require('zope2.View')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    
    def fullname(self):
        context = self.context
        return context.title
         
    
class EditProfile(dexterity.EditForm):
    grok.name('edit-baseinfo')
    grok.context(IMember)    
    label = _(u'Base information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('title','description','email','photo')

class EditProfilePassword(dexterity.EditForm):
    grok.name('edit-password')
    grok.context(IMember)    
    label = _(u'Update password')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IProvidePasswords).select('password','confirm_password')

class EditProfileNetworking(dexterity.EditForm):
    grok.name('edit-networking')
    grok.context(IMember)    
    label = _(u'Network information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('homepage', 'phone','qq_number')
        
class EditProfileWork(dexterity.EditForm):
    grok.name('edit-work')
    grok.context(IMember)    
    label = _(u'Work information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('organization','sector','position','research_domain')

class EditProfileGeography(dexterity.EditForm):
    grok.name('edit-geography')
    grok.context(IMember)    
    label = _(u'Geography information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('country', 'province','address')
    

class EditConfInfo(dexterity.EditForm):
    grok.name('edit-conference')
    grok.context(IMember)    
    label = _(u'conference information')
# avoid autoform functionality
    def updateFields(self):
        pass
    @property
    def fields(self):
        return field.Fields(IMember).select('need_sponsorship', 'roomshare', 'tshirt_size','is_vegetarian','color','comment')    