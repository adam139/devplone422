#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from my315ok.products.testing import MY315OK_PRODUCTS_FUNCTIONAL_TESTING 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
#from eisoo.operation import areafolder
#from eisoo.operation import area
from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestProductsFolderView(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_FUNCTIONAL_TESTING


    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1',
                             PerPagePrdtNum=5,PerRowPrdtNum=3,title="productfolder1",description="demo productfolder")     
     
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="Gif image",description="a gif image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2',title="Jpeg image",description="a jpeg image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3',title="Png image",description="a png image")   
        portal['productfolder1'].invokeFactory('my315ok.products.product','product4',title="Jpeg image2",description="a jpeg image2")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product5',title="Png image2",description="a png image2")               

        data = getFile('image.gif').read()
        item = portal['productfolder1']['product1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        data2 = getFile('image.jpg').read()        
        item2 = portal['productfolder1']['product2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['productfolder1']['product3']
        item3.image = NamedImage(data3, 'image/png', u'image.png') 
        item4 = portal['productfolder1']['product4']
        item4.image = NamedImage(data3, 'image/png', u'image.png')  
        item5 = portal['productfolder1']['product5']
        item5.image = NamedImage(data3, 'image/png', u'image.png')                                 
        self.portal = portal                
        
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        
        import transaction
        transaction.commit()
        
        page = portal.absolute_url() + '/productfolder1'

        browser.open(page)

#        open('/tmp/test.html', 'w').write(browser.contents)

        self.assertTrue('<div id="multiproducts">' in browser.contents)
        
    def test_mediapageview(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        
        import transaction
        transaction.commit()
        
        page = portal.absolute_url() + '/productfolder1/@@mediapageview'

        browser.open(page)
        obj = portal.absolute_url() + '/productfolder1/product1'    
        open('/tmp/test.html', 'w').write(browser.contents)
        outstr = '<a href="%s/@@images/image/large" title="a gif image" class="lightbox">'  % obj

        self.assertTrue(outstr in browser.contents)
        
    def test_barsview(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        page = portal.absolute_url() + '/productfolder1/@@barsview'        
        url1 = portal.absolute_url() + '/productfolder1/product1'
        isrc1 = portal.absolute_url() + '/productfolder1/product1' + "/@@images/image/large"
        title1= "Gif image" 
        url2 = portal.absolute_url() + '/productfolder1/product2'
        isrc2 = portal.absolute_url() + '/productfolder1/product2' + "/@@images/image/large"
        title2= "Jpeg image"  
        url3 = portal.absolute_url() + '/productfolder1/product3'
        isrc3 = portal.absolute_url() + '/productfolder1/product3' + "/@@images/image/large"
        title3= "Png image"                
        browser.open(page)
        lookstr1 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url1,isrc1,title1)
        lookstr2 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url2,isrc2,title2) 
        lookstr3 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url3,isrc3,title3)                
#        import pdb
#        pdb.set_trace()
#        open('/tmp/test.html', 'w').write(browser.contents)

        self.assertTrue(lookstr1 in browser.contents)  
        self.assertTrue(lookstr2 in browser.contents) 
        self.assertTrue(lookstr3 in browser.contents)    

    def test_barsview_mini(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        page = portal.absolute_url() + '/productfolder1/@@barsview_mini'        
        url1 = portal.absolute_url() + '/productfolder1/product1'
        isrc1 = portal.absolute_url() + '/productfolder1/product1' + "/@@images/image/mini"
        title1= "Gif image" 
        url2 = portal.absolute_url() + '/productfolder1/product2'
        isrc2 = portal.absolute_url() + '/productfolder1/product2' + "/@@images/image/mini"
        title2= "Jpeg image"  
        url3 = portal.absolute_url() + '/productfolder1/product3'
        isrc3 = portal.absolute_url() + '/productfolder1/product3' + "/@@images/image/mini"
        title3= "Png image"                
        browser.open(page)
        lookstr1 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url1,isrc1,title1)
        lookstr2 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url2,isrc2,title2) 
        lookstr3 = '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' % (url3,isrc3,title3)                
#        import pdb
#        pdb.set_trace()


        self.assertTrue(lookstr1 in browser.contents)  
        self.assertTrue(lookstr2 in browser.contents) 
        self.assertTrue(lookstr3 in browser.contents)                           