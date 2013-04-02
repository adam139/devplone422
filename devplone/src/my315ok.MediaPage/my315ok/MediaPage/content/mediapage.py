"""Definition of the mediapage content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from my315ok.MediaPage import MediaPageMessageFactory as _
from my315ok.MediaPage.interfaces import Imediapage
from my315ok.MediaPage.config import PROJECTNAME

mediapageSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.StringField(
        'displaymodel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Display Model"),
            description=_(u"select a layou for this media page"),
			format='select',
        ),
        required=True,
        default="right",
        vocabulary=(("right",_(u"image float right")),("left",_(u"image float left")),("banner",_(u"image matrix")))),


    atapi.TextField(
        'text',
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.RichWidget(
            label=_(u"body"),
            description=_(u"a rich textbox that will be a description of the mediapage"),
        ),
        required=True,
    ),


    atapi.StringField(
        'AutoChangeViewLabel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.LabelWidget(
            label=_(u"Configurations for ImageAutoChange View"),
            description=_(u"a configurative page for mediapage"),
        ),
    ),


    atapi.BooleanField(
        'AutoChangeRandom',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"show images randomized"),
            description=_(u"Should we show images randomized in AutoChange views?"),
        ),
        default=0,
    ),


    atapi.StringField(
        'AutoChangeDelay',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"image autochange delay (in milliseconds)"),
            description=_(u"here you can set the delaytime for image autochange view"),
        ),
        default="1000",
    ),


    atapi.StringField(
        'PerPagePrdtNum',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"product numbers will be display in every page(default 12)"),
            description=_(u"here you can set every page display product numbers"),
        ),
        default="12",
    ),


    atapi.StringField(
        'PerRowPrdtNum',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"product numbers will be display in a row(default 4)"),
            description=_(u"here you can set every row display product numbers"),
        ),
        default="4",
    ),


    atapi.BooleanField(
        'UseImageZoom',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"use the image-zoom feature"),
            description=_(u"If you want use the image-zoom feature (Javscript), then check this box."),
        ),
        default=1,
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

mediapageSchema['title'].storage = atapi.AnnotationStorage()
mediapageSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    mediapageSchema,
    folderish=True,
    moveDiscussion=False
)

class mediapage(folder.ATFolder):
    """a free control display model content type"""
    implements(Imediapage)

    meta_type = "mediapage"
    schema = mediapageSchema
    _at_rename_after_creation = True

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    displaymodel = atapi.ATFieldProperty('displaymodel')

    text = atapi.ATFieldProperty('text')

    AutoChangeViewLabel = atapi.ATFieldProperty('AutoChangeViewLabel')

    AutoChangeRandom = atapi.ATFieldProperty('AutoChangeRandom')

    AutoChangeDelay = atapi.ATFieldProperty('AutoChangeDelay')

    PerPagePrdtNum = atapi.ATFieldProperty('PerPagePrdtNum')

    PerRowPrdtNum = atapi.ATFieldProperty('PerRowPrdtNum')

    UseImageZoom = atapi.ATFieldProperty('UseImageZoom')


atapi.registerType(mediapage, PROJECTNAME)
