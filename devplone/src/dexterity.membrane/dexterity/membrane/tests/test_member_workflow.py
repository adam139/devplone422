#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from dexterity.membrane.testing import FUNCTIONAL_TESTING,INTEGRATION_TESTING 

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
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder')
        
        portal['memberfolder'].invokeFactory('dexterity.membrane.member', 'member1',
                             email="12@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 10,
                             description="I am member1")     
        portal['memberfolder'].invokeFactory('dexterity.membrane.member', 'member2',
                             email="13@qq.com",
                             last_name=u"唐",
                             first_name=u"岳军",
                             title = u"tangyuejun",
                             password="391124",
                             confirm_password ="391124",
                             homepae = 'http://315ok.org/',
                             bonus = 300,
                             description="I am member1")   
                               
          
 
        data = getFile('image.jpg').read()
        item = portal['memberfolder']['member1']
        item.photo = NamedImage(data, 'image/jpg', u'image.jpg')
           
        self.portal = portal
    
    def test_member_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'disabled')        
        wf.doActionFor(dummy, 'enable', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'enabled')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'foo')        

              
      
        
   