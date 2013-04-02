from zope.interface import Interface
from zope import schema

from my315ok.products import MessageFactory as _

# Settings stored in the registry

class IMy315okProductsSettings(Interface):
    """Describes registry records
    """
    
    wordsNum = schema.Int(
            title=_(u"max number of word"),
            description=_(u"Allowable max number for product overview"),
#            value_type=schema.TextLine(),
        )
    
class Imarkrichimage(Interface):
    "a mark interface for image that contain title,description,image and rich text fields"
    
class Igoods(Interface):
    "a goods interface for sale in online shop"    