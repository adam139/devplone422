#-*- coding: UTF-8 -*-
import unittest
from zope.schema.vocabulary import SimpleVocabulary
class Testrooms(unittest.TestCase):
    """Unit test for session room field
    """
    def setUp(self):
        self.rooms = [u'东厅',u'南厅',u'西厅',u'北厅']
        
    def test_rooms(self):
        voc = SimpleVocabulary.fromValues(self.rooms)

        self.failUnlessEqual(len(voc),4)