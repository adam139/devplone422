from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class OwaspTheme(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import owasp.theme
        xmlconfig.file('configure.zcml', owasp.theme, context=configurationContext)
        
        # Install products that use an old-style initialize() function

    
    def tearDownZope(self, app):
        # Uninstall products installed above
        pass
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'owasp.theme:default')

OWASP_THEME_FIXTURE = OwaspTheme()
OWASP_THEME_INTEGRATION_TESTING = IntegrationTesting(bases=(OWASP_THEME_FIXTURE,), name="OwaspTheme:Integration")
OWASP_THEME_FUNCTIONAL_TESTING = FunctionalTesting(bases=(OWASP_THEME_FIXTURE,), name="OwaspTheme:Functional")
