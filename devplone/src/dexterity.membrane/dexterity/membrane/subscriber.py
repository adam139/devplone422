#-*- coding: UTF-8 -*-
import json
from five import grok
from time import strftime, localtime 
from zope.component import getMultiAdapter

from dexterity.membrane.interfaces import ICreateMembraneEvent,ICreateBonusRecorderEvent
from dexterity.membrane.content.memberfolder import IMemberfolder
from dexterity.membrane.content.member import IMember
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from Products.DCWorkflow.events import AfterTransitionEvent 

from Products.CMFCore.utils import getToolByName

from plone.dexterity.utils import createContentInContainer

from zope.site.hooks import getSite
from zope.component import getUtility
  

#from Products.CMFCore.Expression import Expression
#from Products.CMFPlone.PloneBaseTool import getExprContext
from Products.PlonePAS.interfaces.events import IUserInitialLoginInEvent

from zope.interface import Interface
from ZODB.POSException import ConflictError
from zExceptions import Forbidden

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as _p
#from collective.singing import mail

#@grok.subscribe(IMember, IObjectModifiedEvent)
#def trigger_member_workflow(member, event):
#    wtool = getToolByName(member, 'portal_workflow')
#    wtool.doActionFor(member, 'autotrigger')

def getMember(context,email):
    catalog = getToolByName(context, "portal_catalog")
    memberbrains = catalog(object_provides=IMember.__identifier__,
                               email=email)

    if len(memberbrains) == 0:return None
    return memberbrains[0].getObject()

@grok.subscribe(IMember, IAfterTransitionEvent)
def sendPasswdResetMail(member, event):
    """
    """
    state = event.new_state.getId()
  
    if state == "enabled":
        registration = getToolByName(member, 'portal_registration')

        email = member.email

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

    memberfolder = newest[0].getObject()
#    import pdb
#    pdb.set_trace()
#    oldid = getattr(memberfolder,'registrant_increment','999999')
#    memberid = str(int(oldid) + 1)
    memberid = event.id        
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
    
@grok.subscribe(Interface, IUserInitialLoginInEvent)
def userInitialLogin(obj, event):
    """Redirects initially logged in users to getting started wizard"""  
    # get portal object
    portal = getSite()  
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return  
    # now complile and render our expression to url

    try:
        member_url_view = getMultiAdapter((portal, request),name=u"member_url") 
        url = member_url_view()
    except Exception, e:
        logException(u'Error during user initial login redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)    

# be call by bonus operation
@grok.subscribe(ICreateBonusRecorderEvent)
def CreateBonusRecorderEvent(event):

    who = event.who  #this should be a email address 

    site = getSite()
    pm = getToolByName(site,'portal_membership')
    userobject=pm.getMemberById(who)
#    userobject = mp.getAuthenticatedMember()
#    username = userobject.getUserName()
#    username = "12@qq.com"    
    recorders = list(userobject.getProperty('bonusrecorder'))
    member = getMember(site,who)
    if not(member  is None):
        who = member.title
        member.bonus = member.bonus + 2
        member.reindexObject()
    recorder = u"%s于%s日，因为%s<a href='%s'>%s<a>而%s%s积分。" %(who,
                                        event.when,
                                        event.what,
                                        event.obj_url,                                        
                                        event.obj_title,
                                        event.result,
                                        event.bonus)        
#    start = datetime.today().strftime('%Y-%m-%d')
#    recorder = "%s 于%s因参加活动<a href='%s'>%s</a>而获取%s积分。" %(username,start,obj.absolute_url(),obj.title,2)
#    
    recorders.append(recorder)
    userobject.setProperties(bonusrecorder=recorders)                        
                            
    
        
