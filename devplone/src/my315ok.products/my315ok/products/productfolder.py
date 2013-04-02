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

from my315ok.products import MessageFactory as _


# Interface class; used to define content-type schema.

class Iproductfolder(form.Schema, IImageScaleTraversable):
    """
    A container that contain multiple products
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/productfolder.xml to define the content type
    # and add directives here as necessary.
    PerPagePrdtNum = schema.Int(
        title=_(u"the number that will be displayed on one page"),
        description=_(u"the number that will be displayed on one page"),
        default=6,
    )
    PerRowPrdtNum = schema.Int(
        title=_(u"product numbers will be display in a row(default 4)"),
        description=(u"here you can set every row display product numbers"),
        default=4,
    )    
    

        
#    form.model("models/productfolder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class productfolder(dexterity.Container):
    grok.implements(Iproductfolder)
    
    # Add your class methods and properties here


