#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from collective.conference.testing import FUNCTIONAL_TESTING
from zope import event

from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager
 
from collective.conference.events import FollowedEvent
from collective.conference.events import RegisteredConfEvent,RegisteredSessionEvent

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
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             title="conference1",
                             description="demo conference1")     

        portal.invokeFactory('collective.conference.conference', 'conference2',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             title="conference2",
                             description="demo conference2") 
        portal.invokeFactory('collective.conference.conference', 'conference4',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             title="conference4",
                             description="demo conference4")  
        portal.invokeFactory('collective.conference.conference', 'conference3',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             title="conference3",
                             description="demo conference3")                         
              
        self.portal = portal

    def test_joined_session_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(RegisteredSessionEvent(portal['conference1']))
        event.notify(RegisteredSessionEvent(portal['conference2']))
        event.notify(RegisteredSessionEvent(portal['conference3']))
        event.notify(RegisteredSessionEvent(portal['conference4']))                        
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@speeches_joined'        

        browser.open(obj)
        outstr = "conference1"
       
        self.assertFalse(outstr in browser.contents)
        outstr = "conference2"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference3"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference4"        
        self.assertTrue(outstr in browser.contents)                        
        
    def test_ajax_session_ifmore(self):
        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(RegisteredSessionEvent(portal['conference1']))
        event.notify(RegisteredSessionEvent(portal['conference2']))
        event.notify(RegisteredSessionEvent(portal['conference3']))
        event.notify(RegisteredSessionEvent(portal['conference4']))         
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 1,    
                        }
        view = self.portal.restrictedTraverse('@@speeches_joined_more')
        result = view()
                     
    def test_joined_conference_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(RegisteredConfEvent(portal['conference1']))
        event.notify(RegisteredConfEvent(portal['conference2']))
        event.notify(RegisteredConfEvent(portal['conference3']))
        event.notify(RegisteredConfEvent(portal['conference4']))                        
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@conferences_joined'        

        browser.open(obj)
        outstr = "conference1"
       
        self.assertFalse(outstr in browser.contents)
        outstr = "conference2"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference3"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference4"        
        self.assertTrue(outstr in browser.contents)                        
        
    def test_ajax_conference_ifmore(self):
        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(RegisteredConfEvent(portal['conference1']))
        event.notify(RegisteredConfEvent(portal['conference2']))
        event.notify(RegisteredConfEvent(portal['conference3']))
        event.notify(RegisteredConfEvent(portal['conference4']))         
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 1,    
                        }
        view = self.portal.restrictedTraverse('@@conferences_joined_more')
        result = view()


## I created conferences
    def test_created_conference_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
                       
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@myconferences'        

        browser.open(obj)
        outstr = "conference1"
       
        self.assertFalse(outstr in browser.contents)
        outstr = "conference2"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference3"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference4"        
        self.assertTrue(outstr in browser.contents)                        
        
    def test_ajax_created_conference_ifmore(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 1,    
                        }
        view = self.portal.restrictedTraverse('@@myconferencesmore')
        result = view()
        self.assertEqual(json.loads(result)['ifmore'],1)
                
    def test_followed_conference_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(FollowedEvent(portal['conference1']))
        event.notify(FollowedEvent(portal['conference2']))
        event.notify(FollowedEvent(portal['conference3']))
        event.notify(FollowedEvent(portal['conference4']))                        
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@followed'        

        browser.open(obj)
        outstr = "conference1"
       
        self.assertFalse(outstr in browser.contents)
        outstr = "conference2"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference3"        
        self.assertTrue(outstr in browser.contents)
        outstr = "conference4"        
        self.assertTrue(outstr in browser.contents)                        
        
    def test_ajax_ifmore(self):
        app = self.layer['app']
        portal = self.layer['portal']
        event.notify(FollowedEvent(portal['conference1']))
        event.notify(FollowedEvent(portal['conference2']))
        event.notify(FollowedEvent(portal['conference3']))
        event.notify(FollowedEvent(portal['conference4']))         
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret, TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'formstart': 1,    
                        }
        view = self.portal.restrictedTraverse('@@followedmore')
        result = view()

        self.assertEqual(json.loads(result)['ifmore'],1)        
        
