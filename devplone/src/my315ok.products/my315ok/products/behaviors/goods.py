from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from my315ok.products import MessageFactory as _


class Igoods(form.Schema):
    """
       Marker/Form interface for goods
    """

    market_price = schema.Float(
                    title=_(u"market price"),
                    default = 0.0,
                    required=False
                                         )
    our_price = schema.Float(
                    title=_(u"our price"),
                    default = 0.0,
                    required=False
                                         )
    brand = schema.TextLine(
                            title=_(u"brand"),
                             )
    model = schema.TextLine(
                            title=_(u"model"),
                             )  
    text = schema.Text(
                            title=_(u"details description"),
                             )            
    # -*- Your Zope schema definitions here ... -*-
    form.fieldset(
                  'sales',
                  label=_(u'sales'),
                  fields=['market_price','our_price','brand','model','text'],
                  )

alsoProvides(Igoods,IFormFieldProvider)

def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)

class goods(object):
    """
       Adapter for productfolder 
    """
    implements(Igoods)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context
    market_price = context_property('market_price')
    our_price = context_property('our_price')
    brand = context_property('brand')
    model = context_property('model')
    text = context_property('text')            
    # -*- Your behavior property setters & getters here ... -*-
