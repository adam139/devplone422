#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.socialorgnization.testing import MY315OK_PRODUCTS_FUNCTIONAL_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
import os
import datetime

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             title="orgnizationfolder1",description="demo orgnizationfolder")     
     
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   legal_person=u"张建明",
                                                   passDate =datetime.datetime.today() 
                                                   )
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','orgnizationsurvey1',
                                                   title=u"宝庆商会1",
                                                   description=u"运输业",
                                                   annual_survey="hege",
                                                   year="2013",

                                                   )  
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','orgnizationsurvey2',
                                                   title=u"宝庆商会2",
                                                   description=u"运输业",
                                                   annual_survey="buhege",
                                                   year="2013",

                                                   )   
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationadministrative','orgnizationadministrative1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   audit_item="chenglidengji",
                                                   audit_result="zhunyu",

                                                   )  
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationadministrative','orgnizationadministrative2',
                                                   title=u"宝庆商会2",
                                                   description=u"运输业",
                                                   audit_item="chenglidengji",
                                                   audit_result="buyu",

                                                   )                         
                  
        self.portal = portal
                

       
    def test_conferencelisting_admin_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['orgnizationfolder1'].absolute_url() + '/@@view'        
        browser.open(obj)

        outstr = "8341"        
        self.assertTrue(outstr in browser.contents)
        
    def test_orgnizaton_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['orgnizationfolder1']['orgnization1'].absolute_url() + '/@@view'        
        browser.open(obj)

        outstr = "8341"        
        self.assertTrue(outstr in browser.contents)        
        
    def test_orgnizations_administrative_view(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['orgnizationfolder1'].absolute_url() + '/@@orgnizations_administrative'        
        browser.open(obj)
        outstr = "oRollV1"        
        self.assertTrue(outstr in browser.contents)        
                    
    def test_oorgnizations_survey_view(self):
        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['orgnizationfolder1'].absolute_url() + '/@@orgnizations_survey'        
        browser.open(obj)
        outstr = "oRollV1"        
        self.assertTrue(outstr in browser.contents)  