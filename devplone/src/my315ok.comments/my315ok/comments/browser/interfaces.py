from zope import schema, interface

from plone.directives import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from my315ok.comments import cMessageFactory as _

class IComment(interface.Interface):
    title = schema.TextLine(title=_(u"Title"))
    author = schema.TextLine(title=_(u"Author"), required=False)
#    form.widget(text=WysiwygFieldWidget)

    text = schema.Text(title=_(u"Text"))                             
   