import os
import tempfile

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig
from plone.testing import z2

class Sandbox(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    PACKAGE = "collective.conference"
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.conference
        import dexterity.membrane
         
        z2.installProduct(app, 'Products.membrane')               
 
        xmlconfig.file('configure.zcml', collective.conference, context=configurationContext)
        xmlconfig.file('configure.zcml', dexterity.membrane, context=configurationContext)        

                      
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'Products.membrane')        
        
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.conference:default')
        applyProfile(portal, 'dexterity.membrane:default')                  
      

TEST_FIXTURE = Sandbox()
INTEGRATION_TESTING = IntegrationTesting(bases=(TEST_FIXTURE,), name="Sandbox:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(TEST_FIXTURE,), name="Sandbox:Functional")
