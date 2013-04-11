#import os
#import tempfile
#
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

from plone.testing import z2

class Sandbox(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    PACKAGE = "dexterity.membrane"
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import dexterity.membrane
 
        xmlconfig.file('configure.zcml', dexterity.membrane, context=configurationContext)
        z2.installProduct(app, 'Products.membrane')
                      
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.membrane')        

    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'dexterity.membrane:default')        
      

TEST_FIXTURE = Sandbox()
INTEGRATION_TESTING = IntegrationTesting(bases=(TEST_FIXTURE,), name="Sandbox:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(TEST_FIXTURE,), name="Sandbox:Functional")
