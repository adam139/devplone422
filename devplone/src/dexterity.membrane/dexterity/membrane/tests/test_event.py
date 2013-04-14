#-*- coding: UTF-8 -*-
import unittest2 as unittest
from zope import event
from collective.conference.testing import INTEGRATION_TESTING
from collective.conference.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from Products.DCWorkflow.events import AfterTransitionEvent


from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

class TestEvent(unittest.TestCase):
    
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
                             bonus = 300,
                             description="I am member1")
                  
        self.portal = portal    
    def test_followed_event(self):
        pass
        
#        file=self.portal['memberfolder']['member1']
#      
#        event.notify(AfterTransitionEvent(file))
        

           

       
class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING