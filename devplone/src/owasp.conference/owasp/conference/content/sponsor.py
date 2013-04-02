import datetime

from zope.interface import invariant, Invalid

from five import grok
from zope import schema

from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IFileFactory

from DateTime import DateTime
from plone.indexer import indexer

from plone.directives import form
from plone.app.textfield import RichText

from plone.formwidget.autocomplete import AutocompleteFieldWidget
from z3c.form.browser.textlines import TextLinesFieldWidget

from owasp.conference import _

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName




class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")


class Isponsor(form.Schema, IImageScaleTraversable):
    """The sponsor for a conference.
    """

    title = schema.TextLine(
            title=_(u"Conference name"),
        )

    description = schema.Text(
            title=_(u"Sponsor summary"),
        )
    
    email = schema.TextLine(
        title=_(u"Email address"),
        required=True,
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
    
    photo = NamedBlobImage(title=_(u'Logo'))  


@form.validator(field=Isponsor['photo'])
def maxPhotoSize(value):
    if value is not None:
        if value.getSize()/1024 > 512:
            raise schema.ValidationError(_(u"Please upload image smaller than 512KB"))



@form.validator(field=Isponsor['email'])
def emailValidator(value):
    try:
        return checkEmailAddress(value)
    except:
        raise Invalid(_(u"Invalid email address"))
