#-*- coding: UTF-8 -*-
import json
from five import grok
from time import strftime, localtime 
from zope.component import getMultiAdapter

from dexterity.membrane.interfaces import ICreateMembraneEvent
from dexterity.membrane.content.memberfolder import IMemberfolder
from dexterity.membrane.content.member import IMember
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Products.DCWorkflow.events import AfterTransitionEvent 

from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer

from zope.site.hooks import getSite
from zope.component import getUtility
from plone.uuid.interfaces import IUUID
from ZODB.POSException import ConflictError
from zExceptions import Forbidden

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p
#from collective.singing import mail

#@grok.subscribe(IMember, IObjectModifiedEvent)
#def trigger_member_workflow(member, event):
#    wtool = getToolByName(member, 'portal_workflow')
#    wtool.doActionFor(member, 'autotrigger')

@grok.subscribe(IMember, IAfterTransitionEvent)
def sendPasswdResetMail(member, event):
    """
    """
    state = event.new_state.getId()
  
    if state == "enabled":
        registration = getToolByName(member, 'portal_registration')

        email = member.email
#        import pdb
#        pdb.set_trace()
        request = member.REQUEST
        
        try:
            response = registration.registeredNotify(email)
            IStatusMessage(request).addStatusMessage(
                        _p(u'create_membrane_account_succesful',
                          default=u"Your account has been created,we "
                          "have sent instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': email}),
                        type='info')
#            return obj            
 
        except ConflictError:
                # Let Zope handle this exception.
                raise            
        except Exception:
                portal = getSite()
                ctrlOverview = getMultiAdapter((portal, request),
                                               name='overview-controlpanel')
                mail_settings_correct = not ctrlOverview.mailhost_warning()
                if mail_settings_correct:
                    # The email settings are correct, so the most
                    # likely cause of an error is a wrong email
                    # address.  We remove the account:
                    # Remove the account:
                    self.context.acl_users.userFolderDelUsers(
                        [user_id], REQUEST=request)
                    IStatusMessage(request).addStatusMessage(
                        _p(u'status_fatal_password_mail',
                          default=u"Failed to create your account: we were "
                          "unable to send instructions for setting a password "
                          "to your email address: ${address}",
                          mapping={u'address': email}),
                        type='error')
                    return
                else:
                    # This should only happen when an admin registers
                    # a user.  The admin should have seen a warning
                    # already, but we warn again for clarity.
                    IStatusMessage(request).addStatusMessage(
                        _p(u'status_nonfatal_password_mail',
                          default=u"This account has been created, but we "
                          "were unable to send instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': email}),
                        type='warning')
                    return    
    else:
        pass

# be call by membrane.usersinout
@grok.subscribe(ICreateMembraneEvent)
def CreateMembraneEvent(event):
    """this event be fired by member join event, username,address password parameters to create a membrane object"""
    site = getSite()
#    mp = getToolByName(site,'portal_membership')
#    members = mp.getMembersFolder()
#    if members is None: return      
    catalog = getToolByName(site,'portal_catalog')
    try:
        newest = catalog.unrestrictedSearchResults({'object_provides': IMemberfolder.__identifier__})
    except:
        return
       
#    from dexterity.membrane.content.member import IMember     
#    try:
#        newest = catalog.unrestrictedSearchResults({'object_provides': IMember.__identifier__,
#                             'sort_order': 'reverse',
#                             'sort_on': 'created',
#                             'sort_limit': 1})
#        if bool(newest): 
#            id = str(int(newest[0].id) + 1)
#        else:
#            id = str(1000000)              
#
#    except:
#            id = str(1000000)
              
#              registrant_increment
    memberfolder = newest[0].getObject()
#    import pdb
#    pdb.set_trace()
    oldid = getattr(memberfolder,'registrant_increment','999999')
    memberid = str(int(oldid) + 1)    
    try:
        item =createContentInContainer(memberfolder,"dexterity.membrane.member",checkConstraints=False,id=memberid)
        setattr(memberfolder,'registrant_increment',memberid)
        item.email = event.email
        item.password = event.password
        item.title = event.title 
        item.description = event.description
        item.homepage = event.homepage
        item.phone = event.phone
        item.organization = event.organization 
        item.sector = event.sector
        item.position = event.position
        item.province = event.province 
        item.address = event.address         

        membrane = getToolByName(item, 'membrane_tool')
        membrane.reindexObject(item)        
    except:
        return

    

        
