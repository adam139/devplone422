import os
import tempfile

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class My315okProducts(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import my315ok.socialorgnization
  
        xmlconfig.file('configure.zcml', my315ok.socialorgnization, context=configurationContext)        

                      
    def tearDownZope(self, app):
        pass
    
    def setUpPloneSite(self, portal):
     
        applyProfile(portal, 'my315ok.socialorgnization:default')
     

MY315OK_PRODUCTS_FIXTURE = My315okProducts()
MY315OK_PRODUCTS_INTEGRATION_TESTING = IntegrationTesting(bases=(MY315OK_PRODUCTS_FIXTURE,), name="My315okProducts:Integration")
MY315OK_PRODUCTS_FUNCTIONAL_TESTING = FunctionalTesting(bases=(MY315OK_PRODUCTS_FIXTURE,), name="My315okProducts:Functional")
