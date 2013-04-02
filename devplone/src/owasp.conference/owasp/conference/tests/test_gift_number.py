import unittest2 as unittest
from eisoo.market.testing import EISOO_MARKET_INTEGRATION_TESTING
from eisoo.market.testing import EISOO_MARKET_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from zope.component import getUtility

class Testgift_number(unittest.TestCase):
    layer =  EISOO_MARKET_INTEGRATION_TESTING    
        
    def test_addgift(self):
        from eisoo.market.interfaces import IMarket_numberLocator      
        locator = getUtility(IMarket_numberLocator)
        locator.AddNumber(12345675,1)