from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from my315ok.portlet.embediframe import EmbedIframePortletMessageFactory as _

scrolling_style=[
('yes','yes',_(u'yes')),
('no','no',_(u'no')),
('auto','auto',_(u'auto')),
  ]
scrolling_style_terms = [
    SimpleTerm(value, token, title) for value, token, title in scrolling_style
]


class ScrollingVocabulary(object):
  """ Ad Unit sizes """

  implements(IVocabularyFactory)

  def __call__(self, context):
      return SimpleVocabulary(scrolling_style_terms)


ScrollingVocabularyFactory = ScrollingVocabulary()
