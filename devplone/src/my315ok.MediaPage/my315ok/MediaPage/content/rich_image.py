"""Definition of the rich_image content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
#from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.image import ATImage,ATImageSchema

# -*- Message Factory Imported Here -*-
from my315ok.MediaPage import MediaPageMessageFactory as _

from my315ok.MediaPage.interfaces import Irich_image
from my315ok.MediaPage.config import PROJECTNAME

rich_imageSchema = ATImageSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.TextField(
        'comment',
        storage=atapi.AnnotationStorage(),
        default_output_type='text/html',
        searchable=True,
        widget=atapi.RichWidget(
            label=_(u"comment details"),
            description=_(u""),
        ),
    ),


    atapi.StringField(
        'link2url',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"link to url"),
            description=_(u""),
        ),
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

rich_imageSchema['title'].storage = atapi.AnnotationStorage()
rich_imageSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(rich_imageSchema, moveDiscussion=False)


class rich_image(ATImage):
    """a image attached rich text comment and a url link"""
    implements(Irich_image)

    meta_type = "rich_image"
    schema = rich_imageSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    comment = atapi.ATFieldProperty('comment')

    link2url = atapi.ATFieldProperty('link2url')


atapi.registerType(rich_image, PROJECTNAME)
