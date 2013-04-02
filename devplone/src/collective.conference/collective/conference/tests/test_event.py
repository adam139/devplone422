import unittest2 as unittest
from zope import event
from collective.conference.testing import INTEGRATION_TESTING
from collective.conference.testing import FUNCTIONAL_TESTING

from Products.CMFCore.utils import getToolByName

from zope.component import getUtility

from collective.conference.events import FollowedEvent
from collective.conference.events import UnfollowedEvent


from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

class TestEvent(unittest.TestCase):
    
    layer = INTEGRATION_TESTING
    
    def test_followed_event(self):
        from collective.conference.conference import IConference
        from collective.conference.interfaces import IEvaluate

        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('collective.conference.conference', 'conference1')
        portal['conference1'].invokeFactory('collective.conference.session', 'session1',
                             description=u"description",
                             additional=u"additional"

                             )
        
        file=portal['conference1']['session1']
        file=portal['conference1']        
        event.notify(FollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        import pdb
        pdb.set_trace()
        questionlist = list(userobject.getProperty('myquestions'))
        evlute = IEvaluate(file)
        
        self.assertTrue(file.id in questionlist)
        
        self.assertTrue(evlute.favavailable(username))
        self.assertEqual(1, evlute.followerNum)
        
        event.notify(UnfollowedEvent(file))
        
        mp = getToolByName(portal,'portal_membership')
        userobject = mp.getAuthenticatedMember()
        username = userobject.getId()
        questionlist = list(userobject.getProperty('myquestions'))
        evlute = IEvaluate(file)
        
        self.assertFalse(file.id in questionlist)
        self.assertFalse(evlute.available(username))
        self.assertEqual(0, evlute.followerNum)



           

       
class TestRendering(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING