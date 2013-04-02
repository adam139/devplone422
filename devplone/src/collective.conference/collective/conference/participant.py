from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFCore.utils import getToolByName

from dexterity.membrane.content.member import IMember

from collective.conference import MessageFactory as _


# Interface class; used to define content-type schema.

class IParticipant(form.Schema, IImageScaleTraversable):
    """
    Conference Participant
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/participant.xml to define the content type
    # and add directives here as necessary.
    title = schema.TextLine(title=_(u"Full name"),
            required=True)
    email = schema.TextLine(
        title=_(u"Email address"),
        required=True,
    )

    description = schema.Text(
        title=_(u"Short Bio"),
        description=_(u"Tell us more about yourself"),
        required=False,
    )

    phone = schema.TextLine(
        title=_(u"Phone number"),
        required=False
    )

    organization = schema.TextLine(
        title=_(u"Organization / Company"),
        required=False,
    )

    position = schema.TextLine(
        title=_(u"Position / Role in Organization"),
        required=False,
    )

    country = schema.Choice(
        title=_(u"Country"),
        description=_(u"Where you are from"),
        required=False,
        vocabulary="collective.conference.vocabulary.countries"
    )



    is_vegetarian = schema.Bool(
        title=_(u"Vegetarian?"),
        required=False
    )

    tshirt_size = schema.Choice(
        title=_(u"T-shirt size"),
        vocabulary="collective.conference.vocabulary.tshirtsize",
        required=False
    )

    photo = NamedBlobImage(
        title=_(u"Photo"),
        description=_(u"Your photo or avatar. Recommended size is 150x195"),
        required=False
    )

    form.fieldset('sponsorship',
            label=_(u"Funding"),
            fields=['need_sponsorship', 'roomshare', 'comment']
    )

    need_sponsorship = schema.Bool(
            title=_(u"Need funding"),
            description=_(u"Check this option if you need funding to attend."), required=False)

    roomshare = schema.Bool(
            title=_(u"Roomshare"),
            description=_(u"If you want or need a room, check this option"),
            required=False)

    comment = schema.Text(
        title=_(u"Comments"),
        description=_(u"Fill in this field with things you need the organizers to know.\
        If you are roomsharing and already have a roommate, please mention your roommate's name here"),
        required=False
    )

    form.widget(color="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    color = schema.TextLine(
        title=_(u"Person Color Tag"),
        default=u'cccccc',
        required=False
    )




@form.validator(field=IParticipant['photo'])
def maxPhotoSize(value):
    if value is not None:
        if value.getSize()/1024 > 512:
            raise schema.ValidationError(_(u"Please upload image smaller than 512KB"))



@form.validator(field=IParticipant['email'])
def emailValidator(value):
    try:
        return checkEmailAddress(value)
    except:
        raise Invalid(_(u"Invalid email address"))

class Participant(dexterity.Item):
    grok.implements(IParticipant)
    grok.provides(IParticipant)


    def sessions(self):
        catalog = getToolByName(self, 'portal_catalog')
        result =  catalog({
            'path': {
                'query': '/'.join(self.getConference().getPhysicalPath()),
                'depth': 2
            }, 'portal_type': 'collective.conference.session',
            'emails': self.email
        })
        return [i.getObject() for i in result]
