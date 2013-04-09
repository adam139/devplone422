#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from collective.conference.testing import FUNCTIONAL_TESTING 

from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('collective.conference.conference', 'conference1',
                             province="beijing",
                             conference_type="Regional Events",
                             address=u"长安街",
                             startDate="2013/03/28",
                             title="conference1",
                             description="demo conference1")    
        portal.invokeFactory('collective.conference.conference', 'conference2',
                             province="hunan",
                             conference_type="Regional Events",
                             address=u"长安街",
                             startDate="2013/03/29",
                             title="conference2",
                             description="demo conference2")  
        portal.invokeFactory('collective.conference.conference', 'conference3',
                             province="heilongjiang",
                             conference_type="Regional Events",
                             address=u"长安街",
                             startDate="2013/03/29",
                             title="conference3",
                             description="demo conference3")          
                 
     
        portal['conference1'].invokeFactory('collective.conference.session','session1',
                                            title="Gif image",
                                            sponsor="IBM",
                                            description="a gif image")
        portal['conference1'].invokeFactory('collective.conference.session',
                                            'session2',
                                            title="Jpeg image",
                                            sponsor="HP",
                                            description="a jpeg image")
        portal['conference1'].invokeFactory('collective.conference.session','session3',
                                            title="Png image",
                                            sponsor="联通",
                                            description="a png image")        

        data = getFile('image.gif').read()
        item = portal['conference1']
        item.logo_image = NamedImage(data, 'image/gif', u'image.gif')
        data2 = getFile('image.jpg').read()        
        item2 = portal['conference2']
        item2.logo_image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['conference3']
        item3.logo_image = NamedImage(data3, 'image/png', u'image.png')                
        self.portal = portal
        
    def test_ajax_voc(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'start': 0,
                        'size':10 ,
                        'datetype':'3',                                                
                        'province': '4',
                        'type': '1',
                        'sortcolumn':'conference_startDate',
                        'sortdirection':'reverse',
                        'searchabletext':'conference1',
                                                                       
                        }
        view = self.portal.restrictedTraverse('@@ajax-conference-type')
        result = view()

        self.assertEqual(json.loads(result), {
                                          'typelist': [["Regional Events", "Regional Events"], ["OWASP Conference", "OWASP Conference"], ["Topic Research", "Topic Research"]],
                                          }) 
        view = self.portal.restrictedTraverse('@@ajax-conference-province')
        result = view()
      
        self.assertEqual(json.loads(result), {
                                          'provincelist':u"<span name='1'><a href='javascript:void(0)'>\u6e56\u5357</a></span><span name='2'><a href='javascript:void(0)'>\u6e56\u5317</a></span><span name='4'><a href='javascript:void(0)'>\u9ed1\u9f99\u6c5f</a></span><span name='5'><a href='javascript:void(0)'>\u5409\u6797</a></span><span name='6'><a href='javascript:void(0)'>\u8fbd\u6797</a></span><span name='7'><a href='javascript:void(0)'>\u5c71\u4e1c</a></span><span name='8'><a href='javascript:void(0)'>\u5c71\u897f</a></span><span name='9'><a href='javascript:void(0)'>\u6cb3\u5317</a></span><span name='10'><a href='javascript:void(0)'>\u6cb3\u5357</a></span><span name='11'><a href='javascript:void(0)'>\u5185\u8499\u53e4</a></span><span name='12'><a href='javascript:void(0)'>\u65b0\u7586</a></span><span name='13'><a href='javascript:void(0)'>\u9752\u6d77</a></span><span name='14'><a href='javascript:void(0)'>\u897f\u85cf</a></span><span name='15'><a href='javascript:void(0)'>\u5c71\u897f</a></span><span name='16'><a href='javascript:void(0)'>\u5929\u6d25</a></span><span name='18'><a href='javascript:void(0)'>\u5b89\u5fbd</a></span><span name='19'><a href='javascript:void(0)'>\u6c5f\u82cf</a></span><span name='20'><a href='javascript:void(0)'>\u6d59\u6c5f</a></span><span name='21'><a href='javascript:void(0)'>\u56db\u5ddd</a></span><span name='22'><a href='javascript:void(0)'>\u798f\u5efa</a></span><span name='24'><a href='javascript:void(0)'>\u5e7f\u897f</a></span><span name='25'><a href='javascript:void(0)'>\u4e91\u5357</a></span><span name='26'><a href='javascript:void(0)'>\u8d35\u5dde</a></span><span name='28'><a href='javascript:void(0)'>\u9999\u6e2f</a></span><span name='29'><a href='javascript:void(0)'>\u6fb3\u95e8</a></span><span name='30'><a href='javascript:void(0)'>\u53f0\u6e7e</a></span><span name='31'><a href='javascript:void(0)'>\u91cd\u5e86</a></span><span name='32'><a href='javascript:void(0)'>\u6c5f\u897f</a></span><span name='33'><a href='javascript:void(0)'>\u5b81\u590f</a></span><span name='34'><a href='javascript:void(0)'>\u7518\u8083</a></span><span name='35'><a href='javascript:void(0)'>\u6d77\u5357</a></span>",
                                          })                       
        
    def test_ajax_search(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'start': 0,
                        'size':10 ,
                        'datetype':'0',                                                
                        'province': '0',
                        'type': '0',
                        'sortcolumn':'conference_startDate',
                        'sortdirection':'reverse',
                        'searchabletext':'conference1',
                                                                       
                        }
# Look up and invoke the view via traversal
        view = self.portal.restrictedTraverse('@@ajaxsearch')
        result = view()

        self.assertEqual(json.loads(result)['size'],10)

               

