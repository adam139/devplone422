import unittest2 as unittest
#from eisoo.mpsource.interfaces import IUserLocator
from owasp.conference.testing import INTEGRATION_TESTING
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

        portal.invokeFactory('owasp.conference.sponsor', 'sponsor1',
                             email=u"a@bb.cc",
                             phone=u"52852385",
                             organization=u"tonglian",
                             position=u"CTO",
                             contry=u"China",
                             )
        data = getFile('image.jpg').read()
        item = portal['sponsor1']
        item.photo = NamedImage(data, 'image/png', u'image.jpg')        
        
        portal['sponsor1'].invokeFactory('owasp.conference.conference','conference1',
                                         title=u"conference1",
                                         description=u"a conference",
                                         details=u"",
                                         start="2013-01-12",
                                         end="2013-02-22",
                                         )

        item = portal['sponsor1']['conference1']
        item.logo_image = NamedImage(data, 'image/png', u'image.jpg')
        del data          
        
 
        self.portal = portal
                
    def test_folder(self):
        self.assertEqual(self.portal['sponsor1'].id,'sponsor1')
    
    def test_conference(self):
        self.assertEqual(self.portal['sponsor1']['conference1'].id,'conferrence1')
        
      
    
        