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

from collective.conference.testing import INTEGRATION_TESTING

from collective.conference import indexer as catalog
from plone.indexer.delegate import DelegatingIndexerFactory

from zope import event
from collective.conference.events import FollowedEvent
from collective.conference.events import UnfollowedEvent

from plone.namedfile.file import NamedImage
import os
def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class CatalogSetupTest(unittest.TestCase):

    layer = INTEGRATION_TESTING
    
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('collective.conference.conference','conference1',
                                         title=u"conference1",
                                         description=u"a conference",
                                         province=u"Beijing",                                         
                                         rooms=[u'room1',u'room2',u'大同',u'\u5927\u5385'],

                                         )
        data = getFile('image.jpg').read()
        item = portal['conference1']
        item.logo_image = NamedImage(data, 'image/png', u'image.jpg')        
        
        portal['conference1'].invokeFactory('collective.conference.session','session1',
                                         title=u"session1",
                                         description=u"a session1",
                                         email=u"adam@qq.com",
                                         conference_rooms=[u'\u5927\u5385'],
                                         text=u"plone session",
                                         )
        portal['conference1'].invokeFactory('collective.conference.session','session2',
                                         title=u"session2",
                                         description=u"a session1",
                                         email=u"adam@qq.com",
                                         conference_rooms=[u'大同'],
                                         text=u"plone session",
                                         )        

        del data 
        self.portal = portal
                 
    
    def test_catalog_installed(self):
        self.assertTrue('id' in
                        self.portal.portal_catalog.indexes())        
        self.assertTrue('conference_rooms' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('conference_province' in
                        self.portal.portal_catalog.indexes()) 
        self.assertTrue('conference_startDate' in
                        self.portal.portal_catalog.indexes())
        self.assertTrue('followernum' in
                        self.portal.portal_catalog.indexes())        
        self.assertTrue('emails' in
                        self.portal.portal_catalog.indexes())                       

    def test_index_value(self):
#        import pdb
#        pdb.set_trace
        self.assertTrue(isinstance(catalog.s_conference_rooms,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.c_conference_rooms,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.c_conference_province,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.c_conference_startDate,
                                DelegatingIndexerFactory))
        self.assertTrue(isinstance(catalog.followernum,
                                DelegatingIndexerFactory))        
        self.assertTrue(isinstance(catalog.p_emails,
                                DelegatingIndexerFactory))
        
        c1 = self.portal['conference1']                                        
        p1 = self.portal['conference1']['session1']
        p2 = self.portal['conference1']['session2']        
#        import pdb
        event.notify(FollowedEvent(c1))
        self.assertEqual(catalog.c_conference_province(c1)(), u'Beijing')
        self.assertEqual(catalog.followernum(c1)(), 1)        
        self.assertEqual(catalog.s_conference_rooms(p1)(), [u'\u5927\u5385'])
        self.assertEqual(catalog.s_conference_rooms(p2)(), [u'大同'])        

    def test_catalogsearch(self):   
        catalog2 = getToolByName(self.portal, 'portal_catalog')     

        results2 = list(catalog2({'conference_rooms': [u'\u5927\u5385']}))
        self.assertEqual(len(results2), 2)
        c1 = self.portal['conference1']          
        event.notify(FollowedEvent(c1))        
        results2 = list(catalog2({'followernum': 1}))
        self.assertEqual(len(results2), 1)
        event.notify(UnfollowedEvent(c1))                 
        results2 = list(catalog2({'followernum': 0}))
        self.assertEqual(len(results2), 1)    

        
       
         
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
