import os
import tempfile

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class My315okPortletRollitems(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import my315ok.portlet.rollitems
  
        xmlconfig.file('configure.zcml', my315ok.portlet.rollitems, context=configurationContext)        

                      
    def tearDownZope(self, app):
        pass
    
    def setUpPloneSite(self, portal):
     
        applyProfile(portal, 'my315ok.portlet.rollitems:default')
     

MY315OK_PORTLET_ROLLITEMS_FIXTURE = My315okPortletRollitems()
MY315OK_PORTLET_ROLLITEMS_INTEGRATION_TESTING = IntegrationTesting(bases=(MY315OK_PORTLET_ROLLITEMS_FIXTURE,), name="My315okPortletRollitems:Integration")
MY315OK_PORTLET_ROLLITEMS_FUNCTIONAL_TESTING = FunctionalTesting(bases=(MY315OK_PORTLET_ROLLITEMS_FIXTURE,), name="My315okPortletRollitems:Functional")
