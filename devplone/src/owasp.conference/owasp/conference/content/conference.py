
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


class Iconference(form.Schema, IImageScaleTraversable):
    """A conference program. Programs can contain Sessions.
    """

    title = schema.TextLine(
            title=_(u"Conference name"),
        )

    description = schema.Text(
            title=_(u"Conference summary"),
        )
    
    logo_image = NamedBlobImage(title=_(u'Logo'))  
    
    address = schema.Text(
            title=_(u"Conference detail address"),
        )      

    start = schema.Datetime(
            title=_(u"Start date"),
            required=False,
        )

    end = schema.Datetime(
            title=_(u"End date"),
            required=False,
        )

    form.primary('details')
    details = RichText(
            title=_(u"Details"),
            description=_(u"Details about the conference"),
            required=False,
        )

    form.widget(organizer=AutocompleteFieldWidget)
    organizer = schema.Choice(
            title=_(u"Organiser"),
            vocabulary=u"plone.principalsource.Users",
            required=False,
        )

    form.widget(tracks=TextLinesFieldWidget)
    tracks = schema.List(
            title=_(u"Tracks"),
            required=True,
            default=[],
            value_type=schema.TextLine(),
        )

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))


@form.default_value(field=Iconference['start'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=Iconference['end'])
def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)

# Indexers


@indexer(Iconference)
def startIndexer(obj):
    if obj.start is None:
        return None
    return DateTime(obj.start.isoformat())
grok.global_adapter(startIndexer, name="start")


@indexer(Iconference)
def endIndexer(obj):
    if obj.end is None:
        return None
    return DateTime(obj.end.isoformat())
grok.global_adapter(endIndexer, name="end")


@indexer(Iconference)
def tracksIndexer(obj):
    return obj.tracks
grok.global_adapter(tracksIndexer, name="Subject")


# Views





