from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from my315ok.portlet.onlineservice import OnlineServiceMessageFactory as _


unit=[
('float','trace mouse float',_(u'trace mouse float')),
('fromtop','stay on top',_(u'stay on top')),
  ]
terms = [
    SimpleTerm(value, token, title) for value, token, title in unit
]


class FloatStyleVocabulary(object):
    
    """ Ad Unit sizes """

    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(terms)


FloatStyleVocabularyFactory = FloatStyleVocabulary()


