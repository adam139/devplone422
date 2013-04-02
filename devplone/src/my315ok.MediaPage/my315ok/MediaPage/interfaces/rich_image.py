from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from my315ok.MediaPage import MediaPageMessageFactory as _


class Irich_image(Interface):
    """a image attached rich text comment and a url link"""

    # -*- schema definition goes here -*-
    comment = schema.SourceText(
        title=_(u"comment details"),
        required=False,
        description=_(u""),
    )
#
    link2url = schema.TextLine(
        title=_(u"link to url"),
        required=False,
        description=_(u""),
    )
#
