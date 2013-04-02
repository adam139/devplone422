from plonetheme.oa.tests.base import SunburstTestCase as TestCase


class SunburstTestCase(TestCase):

    def test_sunburst_layers_available(self):
        self.failUnless('oa_images' in self.portal.portal_skins)
        self.failUnless('oa_styles' in self.portal.portal_skins)
        self.failUnless('oa_templates' in self.portal.portal_skins)

    def test_sunburst_skin_installed(self):
        self.skins = self.portal.portal_skins
        theme = self.skins.getDefaultSkin()
        self.failUnless(theme == 'OA Theme', 'Default theme is %s' % theme)


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
