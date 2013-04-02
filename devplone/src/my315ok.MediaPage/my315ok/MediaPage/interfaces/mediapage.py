from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from my315ok.MediaPage import MediaPageMessageFactory as _

class Imediapage(Interface):
    """a free control display model content type"""
    
    # -*- schema definition goes here -*-
    displaymodel = schema.TextLine(
        title=_(u"Display Model"), 
        required=True,
        description=_(u""),
    )

    text = schema.Text(
        title=_(u"body"), 
        required=True,
        description=_(u""),
    )

    AutoChangeViewLabel = schema.TextLine(
        title=_(u"Configurations for ImageAutoChange View"), 
        required=False,
        description=_(u""),
    )

    AutoChangeRandom = schema.Bool(
        title=_(u"show images randomized"), 
        required=False,
        description=_(u"Should we show images randomized in AutoChange views?"),
    )

    AutoChangeDelay = schema.TextLine(
        title=_(u"image autochange delay (in milliseconds)"), 
        required=False,
        description=_(u"here you can set the delaytime for image autochange view"),
    )

    PerPagePrdtNum = schema.TextLine(
        title=_(u"product numbers will be display in every page(default 12)"), 
        required=False,
        description=_(u"here you can set every page display product numbers"),
    )

    PerRowPrdtNum = schema.TextLine(
        title=_(u"product numbers will be display in a row(default 4)"), 
        required=False,
        description=_(u"here you can set every row display product numbers"),
    )

    UseImageZoom = schema.Bool(
        title=_(u"use the image-zoom feature"), 
        required=False,
        description=_(u"If you want use the image-zoom feature (Javscript), then check this box."),
    )

