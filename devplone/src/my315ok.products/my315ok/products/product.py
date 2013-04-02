from five import grok
from plone.directives import dexterity, form
from plone.multilingualbehavior import directives

from zope import schema
from zope.component import queryUtility
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.indexer import indexer
from plone.memoize.instance import memoize

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText
#
#from z3c.relationfield.schema import RelationList, RelationChoice
#from plone.formwidget.contenttree import ObjPathSourceBinder

from my315ok.products import MessageFactory as _
#from my315ok.products.interfaces import IMy315okProductsSettings 
#from plone.registry.interfaces import IRegistry
#import pdb
#pdb.set_trace()
#registry = queryUtility(IRegistry)
#settings = registry.forInterface(IMy315okProductsSettings, check=False)
#if settings is None:
#    MAX_CONTENT = 200
#else:
#    MAX_CONTENT = settings
MAX_CONTENT = 200    

# Interface class; used to define content-type schema.

class Iproduct(form.Schema, IImageScaleTraversable):
    """
    a product content that contain product image,rich text product spec and product parameters table etc.
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/product.xml to define the content type
    # and add directives here as necessary.
    directives.languageindependent('image')
    image = NamedBlobImage(
        title=_(u"product image"),
        description=_(u"a main image of the product"),
        required=False,        
    )    
    linkurl = schema.TextLine(title=_(u"link to target URI"),
                             default=u"",
                             required=False,)    
    text = RichText(
            title=_(u"details spec of the product"),
            required=True,
        )

#    form.model("models/product.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class product(dexterity.Item):
    grok.implements(Iproduct)
    
    # Add your class methods and properties here

@indexer(Iproduct)
def linkurl(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``content`` index with the linkutrl .
    """
    pview = context.restrictedTraverse('@@plone')

    try:
        url = context.linkurl
    except:
        url = context.absolute_url()
        
    if url == None or "":return ""
    return url

@indexer(Iproduct)
def text(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``content`` index with the answer .
    """
    pview = context.restrictedTraverse('@@plone')

    try:
        text = context.text.output
    except:
        text = context.text
        
    if text == None or "":return ""
    croped = pview.cropText(text, MAX_CONTENT)
    if  isinstance(croped, unicode):
        return croped.encode('utf-8')
    return croped