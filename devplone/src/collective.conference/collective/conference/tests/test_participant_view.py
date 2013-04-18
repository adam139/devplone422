#-*- coding: UTF-8 -*-
from zope import event
from Products.CMFCore.utils import getToolByName
from collective.conference.testing import FUNCTIONAL_TESTING

from collective.conference.events import RegisteredConfEvent 

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
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder')
        
        portal['memberfolder'].invokeFactory('dexterity.membrane.member', 'member1',
                             email="12@qq.com",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")     
     
          
 
        data = getFile('image.jpg').read()
        item = portal['memberfolder']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')        

        portal.invokeFactory('collective.conference.conference', 'conference1',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             title="conference1",
                             startDate = start,
                             endDate = end,
                             text = "conf text",
                             description="demo conference1")     
     
        portal['conference1'].invokeFactory('collective.conference.session','session1',
                                            title="Gif image",
                                            sponsor="IBM",
                                            description="a gif image")
        portal['conference1'].invokeFactory('collective.conference.session',
                                            'session2',
                                            title="Jpeg image",
                                            sponsor="HP",
                                            description="a jpeg image")
        
        portal['conference1'].invokeFactory('collective.conference.participant','participant1',
                                            title="tom",
                                            mail="yuejun.tang@gmail.com",
                                            description="a png image") 
            
        portal['conference1'].invokeFactory('collective.conference.participant','participant2',
                                            title="adam",
                                            mail="yuejun.tang@gmail.com",
                                            description="a png image")            
 
        data = getFile('image.jpg').read()
        item = portal['conference1']
        
        item.logo_image = NamedImage(data, 'image/gif', u'image.gif')
# fire   event for conference      
        event.notify(RegisteredConfEvent(item))        
        data2 = getFile('image.jpg').read()        
        item2 = portal['conference1']['participant1']
        item2.photo = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['conference1']['participant2']
        item3.photo = NamedImage(data3, 'image/png', u'image.png')                
        self.portal = portal
    
    def test_participant_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['conference1']['participant1'].absolute_url() + '/@@view'
        obj = portal['memberfolder']['member1'].absolute_url() + '/@@view'                  

        browser.open(obj)
        outstr = "qq.com"        
        self.assertTrue(outstr in browser.contents)  
        
    def test_participant_list_view(self):         
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['conference1'].absolute_url() + '/@@participants'
                 

        browser.open(obj)
        outstr = "row-fluid"        
        self.assertTrue(outstr in browser.contents)          
   