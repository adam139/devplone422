from plone.registry.interfaces import IRegistry
from zope.component import getMultiAdapter
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from membrane.usersinout.testing import FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest


class TestSettings(unittest.TestCase):
    
    layer = FUNCTIONAL_TESTING
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))           
        self.portal = portal
        
    def test_controlpanel_view(self):
        # Test the setting control panel view works
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="usersinout-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_protected(self):
        # Test that the setting control panel view can not be
        # accessed by anonymous users
        from AccessControl import Unauthorized
        setRoles(self.portal, TEST_USER_ID, ('Member',))  
#        self.logout()
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse,
                                    '@@usersinout-controlpanel')

    def test_entry_in_controlpanel(self):
        # Check that there is a membrane.usersinout entry in the control panel
        controlpanel = getToolByName(self.portal, "portal_controlpanel")
        actions = [a.getAction(self)['id']
                            for a in controlpanel.listActions()]
        self.assertTrue('UsersInOut' in actions)


