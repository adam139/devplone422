#-*- coding: UTF-8 -*-
from five import grok
import json
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.ATContentTypes.interfaces.folder import IATFolder
from plone.memoize.instance import memoize
from collective.conference.interfaces import IEvaluate
from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from Products.AdvancedQuery import Eq, Between, Le
from collective.conference import MessageFactory as _

from collective.conference.conference import IConference
from dexterity.membrane.vocabulary import province_type 

grok.templatedir('templates')

class TopicConferenceListingView(grok.View):
    grok.context(IATTopic)
    grok.template('conference_listing')
    grok.name('conference_listing')

class FolderConferenceListingView(grok.View):
    grok.context(IATFolder)
    grok.template('conference_listing')
    grok.name('conference_listing')

class SiteRootConferenceListingView(grok.View):
    grok.context(ISiteRoot)
    grok.template('conference_listings')
    grok.name('conference_listings')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
#        self.haveHotAnswer = len(self.fetchHotAnswer())>0    
    
    def getconferences(self,num=10):
 
        """返回前num个conference
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        
        maxlen = len(catalog({'object_provides': IConference.__identifier__}))
        if maxlen > num:
            return catalog({'object_provides': IConference.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'created',
                             'sort_limit': num})
        else:
            return catalog({'object_provides': IConference.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})    

    def getHotConferences(self,num=10):
 
        """返回前num个conference
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        
        maxlen = len(catalog({'object_provides': IConference.__identifier__}))
        if maxlen > num:
            return catalog({'object_provides': IConference.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'followernum',
                             'sort_limit': num})
        else:
            return catalog({'object_provides': IConference.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'followernum'})  

class SiteRootAllConferenceListingView(SiteRootConferenceListingView):
    grok.context(ISiteRoot)
    grok.template('allconference_listings')
    grok.name('allconference_listings')
  
                
        
    def test(self,t,a,b):
        """ test method"""   
        if t:
            return a
        else:
            return b
    
    def getconferences(self):
 
        """返回 all conference
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        return catalog({'object_provides': IConference.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})  
    def getType(self,typekey):
        if typekey == 1:
            return "Regional Events"
        elif typekey ==2:
            return "OWASP Conference"
        else:
            return "Topic Research"
         
    def getProvince(self,provincekey):

        pobj = province_type[provincekey - 1][0] 
        return pobj
         
    def search_multicondition(self,query):
        catalog = getToolByName(self.context, 'portal_catalog')
    
        return catalog(query)        

                
 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """
    
    grok.context(ISiteRoot)
    grok.name('ajaxsearch')
    grok.require('zope2.View')

    def Datecondition(self,key):
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        if key == 1:
            end = start 
        elif key == 2:
            end = start + datetime.timedelta(1)
        elif key == 3:
            end = start + datetime.timedelta(7)                                    
        elif key == 4:
            end = start + datetime.timedelta(30)
        else:
            start =  start + datetime.timedelta(30)
            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition
     
    def isFollowed(self,brain):
        obj = brain.getObject()
        aobj = IEvaluate(obj)
        pm = getToolByName(self.context, 'portal_membership')
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        return aobj.available(userid)
    
    def getImageTag(self,brain,scale="thumb"):

        url = brain.getURL() + '/@@images/logo_image/' + scale
        tl = brain.Title
        imgtag = "<img src='%s' alt='%s' />" % (url,tl)

        return imgtag    
          
    def render(self):
    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")        
        
        datadic = self.request.form

        start = int(datadic['start'])
        datekey = int(datadic['datetype'])
        size = int(datadic['size'])                
        provincekey = int(datadic['province'])
        typekey = int(datadic['type'])
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IConference.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
        origquery['b_size'] = size 
        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['conference_province'] = conference_province
        if datekey != 0:
            origquery['conference_startDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['conference_type'] = searchview.getType(typekey)          
#        import pdb
#        pdb.set_trace()
        braindata = searchview.search_multicondition(origquery)            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            description = braindata[i].Description
            objdate = braindata[i].conference_startDate
            sponsor = braindata[i].conference_sponsor            
            objid = braindata[i].id.replace('.','_')
            imgtag = self.getImageTag(braindata[i])

            follow = self.isFollowed(braindata[i])
            if follow:
                followstyle = "display:none;"
                unfollowstyle = "display:inline;"
            else:
                followstyle = "display:inline;"
                unfollowstyle = "display:none;"

            followaction = self.context.absolute_url() + "/@@ajax-follow"
            unfollowaction = self.context.absolute_url() + "/@@ajax-unfollow"

            
            out = """<div class="event_list_search_list row-fluid">
                        <div class="span3">
                            <a href="%(objurl)s" target="_blank" title="%(objtitle)s">%(imgtag)s</a>
                            <div class="row-fluid">
                                <div class="span6">
                                    <span  style="%(followstyle)s" data-ajax-target="%(followaction)s">
                                        <a class="followjq" href="javascript:void()">关注</a>
                                        <input type="text" style="display:none" value="%(objid)s" />
                                    </span>
                                </div>
                                <div class="span6">
                                    <span  style="%(unfollowstyle)s" data-ajax-target="%(unfollowaction)s">
                                        <a class="unfollowjq" href="javascript:void()">取消关注</a>
                                        <input type="text" style="display:none" value="%(objid)s" />
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="span9">
                        <h3>
                            <a href="%(objurl)s"><span>%(objtitle)s</span></a>
                        </h3>
                        <p><span>地点：</span><span>%(objaddress)s</span></p>
                        <p><span>时间：</span><span>%(objdate)s</span></p>
                        <p><span>主办：</span><span>%(sponsor)s</span></p>    
                        <p class="summary">%(description)s<a href="%(objurl)s">详情</a></p>                                                                      
                        </div>
                    </div>"""% dict(objurl=objurl,
                                    objaddress=objtitle,
                                    objtitle=objtitle,
                                    objdate =objdate,
                                    objid = objid,
                                    sponsor = sponsor,
                                    followstyle = followstyle,
                                    unfollowstyle = unfollowstyle,
                                    followaction = followaction,
                                    unfollowaction = unfollowaction,
                                    description = description,
                                    imgtag = imgtag)
                                    
        
#            import pdb
#            pdb.set_trace()             
            outhtml = outhtml + out  

           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':brainnum}
        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)                          