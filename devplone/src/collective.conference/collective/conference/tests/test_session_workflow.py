#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.conference.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
import os

from Products.CMFCore.utils import getToolByName

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import datetime
#        import pdb
#        pdb.set_trace()
        start = datetime.datetime.today()
        end = start + datetime.timedelta(7)
        portal.invokeFactory('collective.conference.conferencefolder', 'conferencefolder')
        
        portal['conferencefolder'].invokeFactory('collective.conference.conference', 'conference1',
                             title = u"conference1",
                             description="I am conference1")
             
        portal['conferencefolder']['conference1'].invokeFactory('collective.conference.session', 'session1',
                             title = u"session1",
                             description="I am sesion1")   
                               

           
        self.portal = portal
    
    def test_conference_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.conference_session_workflow
        conference = portal['conferencefolder']['conference1']
        wf.notifyCreated(conference)

        chain = wf.getChainFor(conference)
        self.failUnless(chain[0] =='conference_session_workflow')

        review_state = wf.getInfoFor(conference, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(conference, 'accept', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(conference, 'review_state')
        self.assertEqual(review_state,'visible')
        comment = wf.getInfoFor(conference, 'comments')
        self.assertEqual(comment,'foo')       
        wf.doActionFor(conference, 'publish', comment='pub' )
        review_state = wf.getInfoFor(conference, 'review_state')
        comment = wf.getInfoFor(conference, 'comments')                        
        self.assertEqual(review_state,'published')
        self.assertEqual(comment,'pub')   
        wf.doActionFor(conference, 'retract', comment='retract')
        comment = wf.getInfoFor(conference, 'comments')
        review_state = wf.getInfoFor(conference, 'review_state')                
        self.assertEqual(review_state,'pending')
        self.assertEqual(comment,'retract')
                       
        wf.doActionFor(conference, 'accept', comment='foo' )
        wf.doActionFor(conference, 'retract', comment='retract' )
        review_state = wf.getInfoFor(conference, 'review_state')
        comment = wf.getInfoFor(conference, 'comments')                        
        self.assertEqual(review_state,'pending')
        self.assertEqual(comment,'retract')          
#    def test_session_workflow(self):
#        app = self.layer['app']
#        portal = self.layer['portal']
#        wf = getToolByName(portal, 'portal_workflow')
#
#        wt = wf.conference_session_workflow
#        session = portal['conferencefolder']['conference1']['session1']
#        wf.notifyCreated(session)
#
#        chain = wf.getChainFor(session)
#        self.failUnless(chain[0] =='conference_session_workflow')
#
#        review_state = wf.getInfoFor(session, 'review_state')
#        self.assertEqual(review_state,'disabled')        
#        wf.doActionFor(session, 'enable', comment='foo' )
#
### available variants is actor,action,comments,time, and review_history        
#        review_state = wf.getInfoFor(session, 'review_state')
#        self.assertEqual(review_state,'enabled')
#        comment = wf.getInfoFor(session, 'comments')
#        self.assertEqual(comment,'foo')                      
#      
        
   