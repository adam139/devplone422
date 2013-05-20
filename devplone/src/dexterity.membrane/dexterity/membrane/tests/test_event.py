#-*- coding: UTF-8 -*-
import unittest2 as unittest
from zope import event
from collective.conference.testing import INTEGRATION_TESTING
from collective.conference.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from Products.DCWorkflow.events import AfterTransitionEvent
from dexterity.membrane.events import CreateBonusRecordEvent


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
        self.start = datetime.datetime.today()
        self.end = self.start + datetime.timedelta(7)
        portal.invokeFactory('dexterity.membrane.memberfolder', 'memberfolder',
                             title='memberfolder',)
        
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
            
    def test_bonus_recorder_event(self):
         
        file=self.portal['memberfolder']['member1']
        pm = getToolByName(self.portal,'portal_membership')
    
        userobject = pm.getAuthenticatedMember()
        userid = userobject.getId()
        when = self.start.strftime('%Y-%m-%d')
        what = "参加活动"
        result = "获取"
        bonus = 2
        recorders = list(userobject.getProperty('bonusrecorder'))
        start_count = len(recorders)  
        event.notify(CreateBonusRecordEvent(userid,when,what,file.title,file.absolute_url(),result,bonus))
        recorders2 = list(userobject.getProperty('bonusrecorder')) 
      
        now_count = len(recorders2)        
        self.assertEqual(start_count + 1,now_count)
       
class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING