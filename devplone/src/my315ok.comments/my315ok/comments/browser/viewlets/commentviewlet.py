from Acquisition import aq_inner

from zope.interface import alsoProvides

from z3c.form.interfaces import IFormLayer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets import ViewletBase

from plone.z3cform import z2

from my315ok.comments.comment import CommentForm
from my315ok.comments import cMessageFactory as _

# starting from 0.6.0 version plone.z3cform has IWrappedForm interface 
try:
    from plone.z3cform.interfaces import IWrappedForm 
    HAS_WRAPPED_FORM = True 
except ImportError: 
    HAS_WRAPPED_FORM = False


class CommentViewlet(ViewletBase):
    index = ViewPageTemplateFile('commentviewlet.pt')
    label = _(u'Add Comment')

    def update(self):
        super(CommentViewlet, self).update()
        z2.switch_on(self, request_layer=IFormLayer)
        self.form = CommentForm(aq_inner(self.context), self.request)
        if HAS_WRAPPED_FORM: 
            alsoProvides(self.form, IWrappedForm)        
        self.form.update()

