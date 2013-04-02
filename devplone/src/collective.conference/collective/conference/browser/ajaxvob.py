
from five import grok
import json
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.interfaces import INavigationRoot

from collective.conference.vocabulary import conference_type 
from dexterity.membrane.vocabulary import province_type

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility 

conference_type_jason = [(value,title) for value, token, title in conference_type]
conference_province_jason = [(value,title) for value, token, title in province_type]



class AjaxConferenceType(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-conference-type')
    grok.require('zope2.View')
        
    def render(self):
        data = {'typelist': conference_type_jason}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
        
class AjaxConferenceProvince(grok.View):
    """AJAX action: follow a question.
    """
    
    grok.context(INavigationRoot)
    grok.name('ajax-conference-province')
    grok.require('zope2.View')
        
    def render(self):
        i = 1
        str = ''
        translation_service = getToolByName(self.context,'translation_service')
        for value, token, title  in province_type:
            # beijin,shanghai guangdong shenzhen skip
            if i in [3,17,23,27]:
                i = i + 1
                continue
            title = translation_service.translate(
                                                  title,
                                                  domain='dexterity.membrane',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="translate")
 
            str += "<span name='%(index)s'><a href='javascript:void(0)'>%(province)s</a></span>" % dict(index=i,province=title)
            i = i + 1            
        data = {'provincelist': str} 
     
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)   
