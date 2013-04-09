import unittest2 as unittest
#from eisoo.mpsource.interfaces import IUserLocator
from collective.conference.testing import INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage
import os
def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('collective.conference.conferencefolder','conferencefolder1')

        portal['conferencefolder1'].invokeFactory('collective.conference.conference','conference1',
                                         title=u"conference1",
                                         description=u"a conference",
                                         rooms=['room1','room2'],

                                         )
        data = getFile('image.jpg').read()
        item = portal['conferencefolder1']['conference1']
        item.logo_image = NamedImage(data, 'image/png', u'image.jpg')        
        
        portal['conferencefolder1']['conference1'].invokeFactory('collective.conference.session','session1',
                                         title=u"session1",
                                         description=u"a session1",
                                         email=u"adam@qq.com",
                                         text=u"plone session",
                                         )

        del data  
        self.portal = portal
    
    def test_conference(self):
        self.assertEqual(self.portal['conferencefolder1']['conference1'].id,'conference1')
        
    def test_session(self):
        self.assertEqual(self.portal['conferencefolder1']['conference1']['session1'].id,'session1')        
        
      
    
        