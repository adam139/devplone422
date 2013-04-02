from zope import interface, schema
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from plone.app.z3cform.layout import FormWrapper
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from my315ok.comments import cMessageFactory as _

import zope.interface
from zope.schema.fieldproperty import FieldProperty
class IComment(zope.interface.Interface):
    title = schema.TextLine(title=_(u"Title"))
    author = schema.TextLine(title=_(u"Author"), required=False)
#    form.widget(text=WysiwygFieldWidget)

    text = schema.Text(title=_(u"Text"))

class Comment(object):
    """
    """

    zope.interface.implements(IComment)

    title= FieldProperty(IComment['title'])
    author = FieldProperty(IComment['author'])
    text = FieldProperty(IComment['text'])
    
class CommentAddForm(form.AddForm):
    """A simple add form for comment."""

    fields = field.Fields(IComment)
#    fields['text'].widgetFactory = WysiwygFieldWidget


    def create(self, data):
        comment = Comment()
        form.applyChanges(self, comment, data)
        return comment

    def add(self, comment):
        self._name = "%s-%s" % (comment.title.lower(), comment.author.lower())
        self.context[self._name] = comment

    def nextURL(self):
        return '/'


class CommentForm(form.AddForm):
    fields = field.Fields(IComment)
    ignoreContext = True # don't use context to get widget data
    label = _(u"Add a comment")
    def create(self, data):
        comment = Comment()
        form.applyChanges(self, comment, data)
        return comment
    def add(self, comment):
        import pdb
        pdb.set_trace()
        self._name = "%s-%s" % (comment.title.lower(), comment.author.lower())
        self.context[self._name] = comment

    def nextURL(self):
        return '/'

    @button.buttonAndHandler(_(u'Post comment'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            return
        if data.has_key('text'):
            self.add(self.create(data))

CommentView = wrap_form(CommentForm)
