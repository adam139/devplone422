#-*- coding: UTF-8 -*-
"""refer  the plone.app.discussion catalog indexes
"""
import unittest2 as unittest

import transaction
from zope import event

from datetime import datetime

from zope.component import createObject
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from my315ok.socialorgnization.testing import MY315OK_PRODUCTS_INTEGRATION_TESTING

from my315ok.socialorgnization import indexer as catalog
from plone.indexer.delegate import DelegatingIndexerFactory

class CatalogSetupTest(unittest.TestCase):

    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1',
                             PerPagePrdtNum=5,PerRowPrdtNum=3,title="orgnizationfolder1",description="demo orgnizationfolder")     
     
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title=u"宝庆商会",
                                                   description=u"运输业",
                                                   address=u"建设北路",
                                                   register_code="8341",
                                                   supervisor=u"交通局",
                                                   organization_type="minfei",
                                                   announcement_type="dengji",                                                   
                                                   law_person=u"张建明",
                                                   passDate="2013-09-18"
                                                   )


        self.portal = portal    
    
    def test_catalog_installed(self):
        self.assertTrue('orgnization_registerCode' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_orgnizationType' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_announcementType' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_passDate' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_annual_survey' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_survey_year' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_audit_item' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('orgnization_audit_result' in
                        self.portal.portal_catalog.indexes())                                                      

    def test_conversation_total_comments(self):
        self.assertTrue(isinstance(catalog.indexer_orgnization_registercode,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.indexer_orgnization_orgnizationtype,
                                DelegatingIndexerFactory))        
        p1 = self.portal['orgnizationfolder1']['orgnization1']
        self.assertEqual(catalog.indexer_orgnization_registercode(p1)(), "8341")

        self.assertEqual(catalog.indexer_orgnization_orgnizationtype(p1)(), "minfei")
        self.assertEqual(catalog.indexer_orgnization_announcementtype(p1)(), "dengji")
        self.assertEqual(catalog.indexer_orgnization_passdate(p1)(), "2013-09-18")                    

    def test_catalogsearch(self):   
        catalog2 = getToolByName(self.portal, 'portal_catalog')     

        results2 = list(catalog2({'orgnization_registerCode': "8341"}))
        self.assertEqual(len(results2), 1)
        results2 = list(catalog2({'orgnization_announcementType': "dengji"}))
        self.assertEqual(len(results2), 1)        
         
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
