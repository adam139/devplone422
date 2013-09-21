from five import grok
from zope import schema

from plone.directives import form, dexterity

from my315ok.socialorgnization import _

class IOrgnizationFolder(form.Schema):
    """
    a folder contain some orgnizations
    """
