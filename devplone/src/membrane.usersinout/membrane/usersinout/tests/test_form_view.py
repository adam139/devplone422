#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
from membrane.usersinout.testing import FUNCTIONAL_TESTING

from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest



class TestView(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))           
        self.portal = portal
    
    def test_form_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal.absolute_url() + '/@@usersinout-controlpanel'        

        browser.open(obj)

        outstr = "form.button.Export"        
        self.assertTrue(outstr in browser.contents)   
        

        
   