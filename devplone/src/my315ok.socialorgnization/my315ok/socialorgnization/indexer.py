from plone.indexer.decorator import indexer
from Products.ZCatalog.interfaces import IZCatalog
from five import grok
from my315ok.socialorgnization.content.orgnization import IOrgnization,IOrgnization_annual_survey,IOrgnization_administrative_licence


@indexer(IOrgnization)
def indexer_orgnization_address(obj, **kw):
    return obj.address

@indexer(IOrgnization)
def indexer_orgnization_legalperson(obj, **kw):
    return obj.legal_person

@indexer(IOrgnization)
def indexer_orgnization_supervisor(obj, **kw):
    return obj.supervisor


@indexer(IOrgnization)
def indexer_orgnization_registercode(obj, **kw):
    return obj.register_code

@indexer(IOrgnization)
def indexer_orgnization_orgnizationtype(obj, **kw):
    return obj.organization_type

@indexer(IOrgnization)
def indexer_orgnization_announcementtype(obj, **kw):
    return obj.announcement_type

@indexer(IOrgnization)
def indexer_orgnization_passdate(obj, **kw):
    return obj.passDate

@indexer(IOrgnization_annual_survey)
def indexer_orgnization_annual_survey(obj, **kw):
    return obj.annual_survey
@indexer(IOrgnization_annual_survey)
def indexer_orgnization_survey_year(obj, **kw):
    return obj.year

@indexer(IOrgnization_administrative_licence)
def indexer_orgnization_audit_item(obj, **kw):
    return obj.audit_item
@indexer(IOrgnization_administrative_licence)
def indexer_orgnization_audit_result(obj, **kw):
    return obj.audit_result




