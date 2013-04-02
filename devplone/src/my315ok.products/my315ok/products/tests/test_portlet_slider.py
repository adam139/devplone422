import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import logout

from my315ok.products.testing import MY315OK_PRODUCTS_INTEGRATION_TESTING

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping

from Products.CMFCore.utils import getToolByName

from my315ok.products.portlets import slidebar_portlet as myportlet

from plone.namedfile.file import NamedImage
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestPortlet(unittest.TestCase):

    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1',
                             PerPagePrdtNum=2,title="productfolder1",description="demo productfolder")     
     
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="Gif image",
                                               linkurl="http://315ok.org/",
                                               description="a gif image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2',title="Jpeg image",description="a jpeg image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3',title="Png image",description="a png image")        

        data = getFile('image.gif').read()
        item = portal['productfolder1']['product1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        data2 = getFile('image.jpg').read()        
        item2 = portal['productfolder1']['product2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['productfolder1']['product3']
        item3.image = NamedImage(data3, 'image/png', u'image.png')                
        self.portal = portal               


    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='my315ok.products.portlets.slidebar_portlet')
        self.assertEquals(portlet.addview, 'my315ok.products.portlets.slidebar_portlet')

    def testInterfaces(self):
        portlet = myportlet.Assignment()
        self.assertTrue(IPortletAssignment.providedBy(portlet))
        self.assertTrue(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portal = self.layer['portal']
        
        portlet = getUtility(IPortletType, name='my315ok.products.portlets.slidebar_portlet')
        mapping = portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
#        import pdb
#        pdb.set_trace()
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

#        addview()
        addview.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.assertTrue(isinstance(mapping.values()[0], myportlet.Assignment))
        
    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = myportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, myportlet.EditForm))        

    def testRenderer(self):
        context = self.layer['portal']
        request = self.layer['request']
        
        view = context.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=context)
        assignment = myportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.assertTrue(isinstance(renderer, myportlet.Renderer))

class TestRenderer(unittest.TestCase):
    
    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.products.productfolder', 'productfolder1',
                             PerPagePrdtNum=2,title="productfolder1",description="demo productfolder")     
     
        portal['productfolder1'].invokeFactory('my315ok.products.product','product1',title="Gif image",
                                               linkurl="http://315ok.org/",                                               
                                               description="a gif image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product2',title="Jpeg image",description="a jpeg image")
        portal['productfolder1'].invokeFactory('my315ok.products.product','product3',title="Png image",description="a png image")        

        data = getFile('image.gif').read()
        item = portal['productfolder1']['product1']
        item.image = NamedImage(data, 'image/gif', u'image.gif')
        data2 = getFile('image.jpg').read()        
        item2 = portal['productfolder1']['product2']
        item2.image = NamedImage(data2, 'image/jpeg', u'image.jpg')  
        data3 = getFile('image.png').read()        
        item3 = portal['productfolder1']['product3']
        item3.image = NamedImage(data3, 'image/png', u'image.png')                
        self.portal = portal 
                    

    
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        portal = self.layer['portal']
        
        context = context or portal
        request = request or self.layer['request']
        
        view = view or portal.restrictedTraverse('@@plone')
        
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=portal)
        assignment = assignment or myportlet.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

