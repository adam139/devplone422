from five import grok
from dexterity.membrane.content.member import IMember
from dexterity.membrane.content.memberfolder import IMemberfolder
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.error import ErrorViewSnippet

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

from Products.statusmessages.interfaces import IStatusMessage
from dexterity.membrane import _
from Products.CMFPlone import PloneMessageFactory as _p


from ZODB.POSException import ConflictError
from zExceptions import Forbidden

class IRegistrationForm(IMember):

    publishinfo = schema.Bool(
        title=_(u"Show me in attendee list"),
        description=_(u"Check this if you wish your name and contact info \
        to be published in our attendee listing"),
        required=False
    )

    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)

    form.omitted('color')

@form.validator(field=IRegistrationForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IRegistrationForm['captcha'], None)
    captcha.validate(value)


class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IMemberfolder)
#    grok.require("zope.Public")
    grok.require('zope2.View')    
    schema = IRegistrationForm
    label = _(u"Register for site member")


    def create(self, data):
        inc = getattr(self.context, 'registrant_increment', 999999) + 1
        data['id'] = '%s' % inc
        self.context.registrant_increment = inc
        obj = _createObjectByType("dexterity.membrane.member", 
                self.context, data['id'])

        publishinfo = data['publishinfo']
        del data['captcha']
        del data['publishinfo']
        for k, v in data.items():
            setattr(obj, k, v)

        registration = getToolByName(self.context, 'portal_registration')
            

#        portal_workflow = getToolByName(self.context, 'portal_workflow')
#        if publishinfo:
#            portal_workflow.doActionFor(obj, 'anon_publish')
#        else:
#            portal_workflow.doActionFor(obj, 'anon_hide')
        obj.reindexObject()
        email = data.get('email', '')
        try:
            response = registration.registeredNotify(email)
            IStatusMessage(self.request).addStatusMessage(
                        _p(u'create_membrane_account_succesful',
                          default=u"Your account has been created,we "
                          "have sent instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': email}),
                        type='info')
            return obj            
 
        except ConflictError:
                # Let Zope handle this exception.
                raise            
        except Exception:
                ctrlOverview = getMultiAdapter((portal, self.request),
                                               name='overview-controlpanel')
                mail_settings_correct = not ctrlOverview.mailhost_warning()
                if mail_settings_correct:
                    # The email settings are correct, so the most
                    # likely cause of an error is a wrong email
                    # address.  We remove the account:
                    # Remove the account:
                    self.context.acl_users.userFolderDelUsers(
                        [user_id], REQUEST=self.request)
                    IStatusMessage(self.request).addStatusMessage(
                        _p(u'status_fatal_password_mail',
                          default=u"Failed to create your account: we were "
                          "unable to send instructions for setting a password "
                          "to your email address: ${address}",
                          mapping={u'address': data.get('email', '')}),
                        type='error')
                    return
                else:
                    # This should only happen when an admin registers
                    # a user.  The admin should have seen a warning
                    # already, but we warn again for clarity.
                    IStatusMessage(self.request).addStatusMessage(
                        _p(u'status_nonfatal_password_mail',
                          default=u"This account has been created, but we "
                          "were unable to send instructions for setting a "
                          "password to this email address: ${address}",
                          mapping={u'address': data.get('email', '')}),
                        type='warning')
                    return                            

    def add(self, obj):
        pass
