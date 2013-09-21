from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
#import unicodedata
#from incf.countryutils import data as countrydata
from my315ok.socialorgnization import _


announcement_type=[    ('chengli','chengli',_(u'chengli')),
                  ('biangeng','biangeng',_(u'biangeng')),
                  ('zhuxiao','zhuxiao',_(u'zhuxiao')),
                        ]
announcement_type_terms = [SimpleTerm(value, token, title) for value, token, title in announcement_type ]

class AnnouncementType(object):

    def __call__(self, context):
        return SimpleVocabulary(announcement_type_terms)

grok.global_utility(AnnouncementType, IVocabularyFactory,
        name="my315ok.socialorgnization.vocabulary.announcementtype")

organization_type=[    ('shetuan','shetuan',_(u'shetuan')),
                  ('minfei','minfei',_(u'minfei')),
                  ('jijinhui','jijinhui',_(u'jijinhui')),
                        ]
organization_type_terms = [SimpleTerm(value, token, title) for value, token, title in organization_type ]

class OrganizationType(object):

    def __call__(self, context):
        return SimpleVocabulary(organization_type_terms)

grok.global_utility(OrganizationType, IVocabularyFactory,
        name="my315ok.socialorgnization.vocabulary.organizationtype")

annualsurvey_result=[    ('hege','hege',_(u'hege')),
                  ('jibenhege','jibenhege',_(u'jibenhege')),
                  ('buhege','buhege',_(u'buhege')),
                        ]
annualsurvey_result_terms = [SimpleTerm(value, token, title) for value, token, title in annualsurvey_result ]

class AnnualsurveyResult(object):

    def __call__(self, context):
        return SimpleVocabulary(annualsurvey_result_terms)

grok.global_utility(AnnualsurveyResult, IVocabularyFactory,
        name="my315ok.socialorgnization.vocabulary.annualsurvey")

audit_item=[    ('chenglidengji','chenglidengji',_(u'chenglidengji')),
                  ('biangengdengji','biangengdengji',_(u'biangengdengji')),
                        ]
audit_item_terms = [SimpleTerm(value, token, title) for value, token, title in audit_item ]

class AuditItem(object):

    def __call__(self, context):
        return SimpleVocabulary(audit_item_terms)

grok.global_utility(AuditItem, IVocabularyFactory,
        name="my315ok.socialorgnization.vocabulary.audit_item")

audit_result=[    ('zhunyu','zhunyu',_(u'zhunyu')),
                  ('buyu','buyu',_(u'buyu')),
                        ]
audit_result_terms = [SimpleTerm(value, token, title) for value, token, title in audit_result ]

class AuditResult(object):

    def __call__(self, context):
        return SimpleVocabulary(audit_result_terms)

grok.global_utility(AuditResult, IVocabularyFactory,
        name="my315ok.socialorgnization.vocabulary.audit_result")



