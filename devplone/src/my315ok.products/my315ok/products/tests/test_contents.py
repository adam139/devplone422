import unittest2 as unittest

from my315ok.products.testing import MY315OK_PRODUCTS_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1')
        
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2')
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3')        


        self.portal = portal
                
    def test_marketfolder(self):
        self.assertEqual(self.portal['productfolder1'].id,'productfolder1')
    

    
    def test_meetapply(self):
        self.assertEqual(self.portal['productfolder1']['product1'].id,'product1')
        
     
    
        