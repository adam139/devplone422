from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class My315okDiaozo960(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import my315ok.diazo960
        xmlconfig.file('configure.zcml', my315ok.diazo960, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'my315ok.diazo960:default')

MY315OK_DIAZO960_FIXTURE = My315okDiaozo960()
MY315OK_DIAZO960_INTEGRATION_TESTING = IntegrationTesting(bases=(MY315OK_DIAZO960_FIXTURE,), name="My315okDiaozo960:Integration")
MY315OK_DIAZO960_FUNCTION_TESTING = FunctionalTesting(bases=(MY315OK_DIAZO960_FIXTURE,), name="My315okDiaozo960:Functional")
