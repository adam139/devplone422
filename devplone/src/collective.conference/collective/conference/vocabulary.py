from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
import unicodedata
from incf.countryutils import data as countrydata
from collective.conference import MessageFactory as _


class TShirtSize(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(
            ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        )

grok.global_utility(TShirtSize, IVocabularyFactory,
        name="collective.conference.vocabulary.tshirtsize")

class Countries(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(sorted([
            i.decode('utf-8') for i,c in countrydata.cn_to_ccn.items() if c != '248'
        ]))

grok.global_utility(Countries, IVocabularyFactory,
        name="collective.conference.vocabulary.countries")

session_type=[    ('Talk','Talk',_(u'Talk')),
                  ('Workshop','Workshop',_(u'Workshop')),
                  ('Discussion','Discussion',_(u'Discussion')),
                        ]
session_type_terms = [SimpleTerm(value, token, title) for value, token, title in session_type ]

class SessionTypes(object):

    def __call__(self, context):
        return SimpleVocabulary(session_type_terms)

grok.global_utility(SessionTypes, IVocabularyFactory,
        name="collective.conference.vocabulary.sessiontype")

conference_type=[    ('Regional Events','Regional Events',_(u'Regional Events')),
                  ('OWASP Conference','OWASP Conference',_(u'OWASP Conference')),
                  ('Topic Research','Topic Research',_(u'Topic Research')),
                        ]
conference_type_terms = [SimpleTerm(value, token, title) for value, token, title in conference_type ]

class ConferenceTypes(object):

    def __call__(self, context):
        return SimpleVocabulary(conference_type_terms)

grok.global_utility(ConferenceTypes, IVocabularyFactory,
        name="collective.conference.vocabulary.conferencetype")

session_level = [ ('Beginner','Beginner',_(u'Beginner')),
                  ('Intermediate','Intermediate',_(u'Intermediate')),
                  ('Advanced','Advanced',_(u'Advanced')),
                        ]
session_level_terms = [SimpleTerm(value, token, title) for value, token, title in session_level ]

class SessionLevels(object):

    def __call__(self, context):
        return SimpleVocabulary(session_level_terms)

grok.global_utility(SessionLevels, IVocabularyFactory,
        name="collective.conference.vocabulary.sessionlevel")

class RoomsVocabulary(object):
    """Creates a vocabulary with the sections stored in the registry; the
    vocabulary is normalized to allow the use of non-ascii characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
#        registry = getUtility(IRegistry)
#        settings = registry.forInterface(INITFSettings)
        conference = context.getConference()
        items = []
        for section in conference.rooms:
            token = unicodedata.normalize('NFKD', section).encode('utf-8', 'ignore').lower()
            items.append(SimpleVocabulary.createTerm(token, token, section))
        return SimpleVocabulary(items)

grok.global_utility(RoomsVocabulary, name=u'collective.conference.rooms')

