#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.ATContentTypes.interfaces.folder import IATFolder
from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _

from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder

from plone.memoize.instance import memoize

from Products.CMFCore import permissions
grok.templatedir('templates') 

class Orgnizations_adminView(grok.View):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_listing_admin')
    grok.name('view')
    grok.require('zope2.View')    
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
    
    @property
    def isEditable(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, 'portal_membership')
        return pm.checkPermission(permissions.ManagePortal,context) 

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='my315ok.socialorgnization',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="chengli")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
        
    @memoize         
    def getOrgnizationFolder(self):
        context = aq_inner(self.context)
        tfc = getToolByName(context, 'portal_catalog')
        topicfolder = tfc({'object_provides': IOrgnizationFolder.__identifier__})
        
        mt = getToolByName(context,'portal_membership')
        canManage = mt.checkPermission(permissions.AddPortalContent,context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath        
        
    @memoize     
    def getMemberList(self):
        """获取申请的会议列表"""
        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog({'object_provides':IOrgnization.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        i = 0
        for brain in memberbrains:
            i = i+1           
            row = {'number':'','id':'', 'name':'', 'url':'',
                    'sponsor':'', 'orgnization_passDate':'', 'legal_person':'','address':'','register_code':'','editurl':'',
                    'delurl':''}
            row['number'] = i
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['sponsor'] = brain.orgnization_supervisor
            row['orgnization_passDate'] = brain.orgnization_passDate.strftime('%Y-%m-%d')
            row['legal_person'] = brain.orgnization_legalPerson            
            row['address'] = brain.orgnization_address
            row['register_code'] = brain.orgnization_registerCode


            row['editurl'] = row['url'] + '/confajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist

class OrgnizationsView(Orgnizations_adminView):
    grok.context(IOrgnization)
    grok.template('orgnization_view')
    grok.name('view')
    grok.require('zope2.View')
    
    def getAnnualSurveyList(self):
        """获取年检结果列表"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            annual_survey = self.tranVoc(braindata[i].orgnization_annual_survey)
            year = braindata[i].orgnization_survey_year

            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            annual_survey= annual_survey,
                                            year=year)           
            outhtml = outhtml + out
        return outhtml             
    
    def getAdministrativeLicenceList(self):
        """获取行政许可列表"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_administrative_licence.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            audit_item = self.tranVoc(braindata[i].orgnization_audit_item)
            audit_result = self.tranVoc(braindata[i].orgnization_audit_result)

            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(audit_item)s</td>
            <td class="result">%(audit_result)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            audit_item= audit_item,
                                            audit_result=audit_result)           
            outhtml = outhtml + out
        return outhtml
    
#年检默认视图    
class AnnualsurveyView(Orgnizations_adminView):
    grok.context(IOrgnization_annual_survey)
    grok.template('orgnization_annual_survey')
    grok.name('view')
    grok.require('zope2.View') 
        
#行政许可默认视图    
class AdministrativeLicenceView(Orgnizations_adminView):
    grok.context(IOrgnization_administrative_licence)
    grok.template('orgnization_administrative_licence')
    grok.name('view')
    grok.require('zope2.View')                

class Orgnizations_annualsurveyView(Orgnizations_adminView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_annual_survey_roll')
    grok.name('orgnizations_survey')
    grok.require('zope2.View')

    @memoize
    def getMemberList(self):
        """获取年检结果列表"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            annual_survey = self.tranVoc(braindata[i].orgnization_annual_survey)
            year = braindata[i].orgnization_survey_year

            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            annual_survey= annual_survey,
                                            year=year)           
            outhtml = outhtml + out
        return outhtml        

           
 
class Orgnizations_administrativeView(Orgnizations_adminView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_administrative_licence_roll')
    grok.name('orgnizations_administrative')
    grok.require('zope2.View')  


    @memoize        
    def getMemberList(self):
        """获取行政许可列表"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_administrative_licence.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )

        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            audit_item = self.tranVoc(braindata[i].orgnization_audit_item)
            audit_result = self.tranVoc(braindata[i].orgnization_audit_result)

            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(audit_item)s</td>
            <td class="result">%(audit_result)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            audit_item= audit_item,
                                            audit_result=audit_result)           
            outhtml = outhtml + out
        return outhtml
             
    
class SiteRootOrgnizationListingView(grok.View):
    grok.context(ISiteRoot)
    grok.template('orgnization_listings')
    grok.name('orgnization_listings')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
  
    
    def getOrgnizationFolder(self):
        context = aq_inner(self.context)
        tfc = getToolByName(context, 'portal_catalog')
        topicfolder = tfc({'object_provides': IOrgnizationFolder.__identifier__})
        
        mt = getToolByName(context,'portal_membership')
        canManage = mt.checkPermission(permissions.AddPortalContent,context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath

    def getorgnizations(self,num=10):
 
        """返回前num个conference
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        
        maxlen = len(catalog({'object_provides': IOrgnization.__identifier__}))
        if maxlen > num:
            return catalog({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'conference_passDate',
                             'sort_limit': num})
        else:
            return catalog({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'conference_passDate'})    

class SiteRootAllOrgnizationListingView(SiteRootOrgnizationListingView):
    grok.context(ISiteRoot)
    grok.template('allorgnization_listings')
    grok.name('allorgnization_listings')
     
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)                
        
    def test(self,t,a,b):
        """ test method"""   
        if t:
            return a
        else:
            return b
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return catalog({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})
#翻译 社团，民非，基金会          
    def getType(self,typekey):
        if typekey == 1:
            return "shetuan"
        elif typekey ==2:
            return "minfei"
        else:
            return "jijinhui"
         
#翻译 成立公告，变更，注销公告  
    def getProvince(self,provincekey):
        if provincekey == 1:
            return "chengli"
        elif provincekey ==2:
            return "biangeng"
        else:
            return "zhuxiao"
         
    def search_multicondition(self,query):
        catalog = getToolByName(self.context, 'portal_catalog')    
        return catalog(query)        

                
 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """    
    grok.context(ISiteRoot)
    grok.name('oajaxsearch')
    grok.require('zope2.View')

    def Datecondition(self,key):        

        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
        origquery['b_size'] = size 
        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        braindata = searchview.search_multicondition(origquery)            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span4">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span1">%(legal_person)s</td>
                                <td class="span1">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':brainnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)                          
