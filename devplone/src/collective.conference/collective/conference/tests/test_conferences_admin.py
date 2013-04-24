#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.conference.testing import FUNCTIONAL_TESTING 

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
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('collective.conference.conferencefolder', 'conferencefolder')
        portal['conferencefolder'].invokeFactory('collective.conference.conference', 'conference1',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             startDate =start,
                             title="conference1",
                             description="demo conference1")   
        portal['conferencefolder'].invokeFactory('collective.conference.conference', 'conference2',
                             province="Beijin",
                             conference_type="Regional Events",
                             address=u"长安街",
                             startDate =end,                             
                             title="conference2",
                             description="demo conference2")                     
        self.portal = portal
                
    def test_conferencelisting_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()

        obj = portal['conferencefolder'].absolute_url() + '/@@view'        
        browser.open(obj)
        outstr = "conference1"        
        self.assertTrue(outstr in browser.contents)
       
    def test_conferencelisting_admin_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['conferencefolder'].absolute_url() + '/@@conferences_admin'        
        browser.open(obj)
        outstr = "row-fluid"        
        self.assertTrue(outstr in browser.contents)        
