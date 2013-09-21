#-*- coding: UTF-8 -*-
from five import grok
from zope import schema
from zope.interface import Interface
import datetime

from plone.directives import form, dexterity
from plone.app.dexterity.behaviors.metadata import IBasic
from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary

from collective import dexteritytextindexer

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
#from collective.dexteritytextindexer.behavior import IDexterityTextIndexer

from my315ok.socialorgnization import _

class IOrgnization(form.Schema,IBasic):
    """
    orgnization content type
    """
#名称
    dexteritytextindexer.searchable('title')    
    title = schema.TextLine(title=_(u"orgnization name"),
                             default=u"",
                            required=True,) 
#经营范围        
    description = schema.TextLine(title=_(u"sector"),
                             default=u"",
                             required=False,)
#   住所 
    address = schema.TextLine(title=_(u"Address"),
                             default=u"",
                             required=False,)
#   法人     
    legal_person = schema.TextLine(title=_(u"legal person"),
                             default=u"",
                             required=False,)
# 主管单位    
    supervisor = schema.TextLine(title=_(u"supervisor organization"),
                             default=u"",
                             required=False,)    
#登记证号    
    register_code = schema.ASCIILine(
            title=_("label_register_code",
                default=u"register code"),
            description=_("help_register_code",
                default=u"A code identifying this sector. register "
                        u"codes are defined by national standards bodies "
                        u"and based on revision 2 of the NACE standard."),
            required=True)
#组织类别            
    organization_type = schema.Choice(
        title=_(u"organization Type"),
        vocabulary="my315ok.socialorgnization.vocabulary.organizationtype"
    )
#公告类别：成立/变更/注销            
    announcement_type = schema.Choice(
        title=_(u"announcement Type"),
        vocabulary="my315ok.socialorgnization.vocabulary.announcementtype"
    ) 
# 批准日期

    passDate = schema.Datetime(
        title=_(u"Pass Date"),
        description=u'',
        required=True,
    )

class ICostomTitle(Interface):
    """Get the name from parent object's id.
    This is really just a marker interface.
    """
@grok.provider(IContextSourceBinder)
def possibleOrganization(context):
         

    terms = []
    value = context.title  # I'm assuming these values are Unicode
    terms.append(SimpleTerm(value,
                                token=value.encode('unicode_escape'), title=value))
    return SimpleVocabulary(terms)
    
class IOrgnization_annual_survey(form.Schema,IBasic):

##所属社会组织
#    title = schema.Choice(
#            title=_(u"organization name"),
#            source=DynamicVocabulary("my315ok.socialorgnization.content.orgnization", "IOrgnization",name="title")
#                        ) 
    title = schema.Choice(
        title=_(u"organization name"),     
        source=possibleOrganization,     
        required=True
    )
   
#年检结果            
    annual_survey = schema.Choice(
        title=_(u"the result of annual survey"),
        vocabulary="my315ok.socialorgnization.vocabulary.annualsurvey"
    )
    
#年度           
    year = schema.TextLine(title=_(u"the year for survey"),
                             default=u"",
                             required=False,)
    form.omitted('description')    

class IOrgnization_administrative_licence(form.Schema,IBasic):

##所属社会组织
#    title = schema.Choice(
#            title=_(u"organization name"),
#            source=DynamicVocabulary("my315ok.socialorgnization.content.orgnization", "IOrgnization",name="title")
#                        )
    title = schema.Choice(
        title=_(u"organization name"),     
        source=possibleOrganization,     
        required=True
    )
#许可事项            
    audit_item = schema.Choice(
        title=_(u"the item had been audited"),
        vocabulary="my315ok.socialorgnization.vocabulary.audit_item"
    )
    
#结果          
    audit_result = schema.Choice(
                                 title=_(u"the result of item that had been audited"),
                                 vocabulary="my315ok.socialorgnization.vocabulary.audit_result",                                 
                                 default=u"",
                                 required=False,) 
    form.omitted('description')       
    
@form.default_value(field=IOrgnization['passDate'])
def passDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(-1)           