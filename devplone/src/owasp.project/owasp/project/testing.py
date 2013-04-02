from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class OwaspProject(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import owasp.project
        xmlconfig.file('configure.zcml', owasp.project, context=configurationContext)
        

    def tearDownZope(self, app):
        # Uninstall products installed above
        pass
        
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'owasp.project:default')

OWASP_PROJECT_FIXTURE = OwaspProject()
OWASP_PROJECT_INTEGRATION_TESTING = IntegrationTesting(bases=(OWASP_PROJECT_FIXTURE,), name="OwaspProject:Integration")
OWASP_PROJECT_FUNCTIONAL_TESTING = FunctionalTesting(bases=(OWASP_PROJECT_FIXTURE,), name="OwaspProject:Functional")
