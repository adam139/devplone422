from DateTime import DateTime
import datetime
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from zope.interface import invariant, Invalid
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.miscbehaviors import _
from collective.miscbehaviors.behavior.utils import context_property

from collective import dexteritytextindexer

class StartBeforeEnd(Invalid):
    __doc__ = _(u"The start or end date is invalid")

class IStartEndDate(form.Schema):
    """
        Marker/Form interface for Start/End Dates
    """
   
    # -*- Your Zope schema definitions here ... -*-

    startDate = schema.Datetime(
        title=_(u"Start Date"),
        description=u'',
        required=True,
    )

    endDate = schema.Datetime(
        title=_(u"End Date"),
        description=u'',
        required=True,
    )
    
    @invariant
    def validateStartEnd(data):
        if data.startDate is not None and data.endDate is not None:
            if data.startDate > data.endDate:
                raise StartBeforeEnd(_(
                    u"The start date must be before the end date."))
@form.default_value(field=IStartEndDate['startDate'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=IStartEndDate['endDate'])
def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)

alsoProvides(IStartEndDate,IFormFieldProvider)


class StartEndDate(object):
    """
      Adapter for Start/End Dates
    """
    implements(IStartEndDate)
    adapts(IDexterityContent)

    def __init__(self,context):
       self.context = context

    # -*- Your behavior property setters & getters here ... -*-

    startDate = context_property('startDate')
    endDate = context_property('endDate')
