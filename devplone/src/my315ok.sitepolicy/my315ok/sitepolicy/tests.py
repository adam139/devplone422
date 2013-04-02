import unittest2 as unittest
from eisoo.policy.testing import EISOO_POLICY_INTEGRATION_TESTING

from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = EISOO_POLICY_INTEGRATION_TESTING
    
#    def test_portal_title(self):
#        portal = self.layer['portal']
#        self.assertEqual("Eisoo kCRM", portal.getProperty('title'))
#    
#    def test_portal_description(self):
#        portal = self.layer['portal']
#        self.assertEqual("Welcome to Eisoo kCRM", portal.getProperty('description'))
    
    def test_role_added(self):
        portal = self.layer['portal']
        self.assertTrue("Knowledge Manager" in portal.validRoles())
        self.assertTrue("Maintenance Engineer" in portal.validRoles())
#    
#    def test_workflow_installed(self):
#        portal = self.layer['portal']
#        workflow = getToolByName(portal, 'portal_workflow')
#        
#        self.assertTrue('eisoo_forum_workflow' in workflow)
#        self.assertTrue('eisoo_knowledge_workflow' in workflow)

    def test_workflows_mapped(self):
        portal = self.layer['portal']
        workflow = getToolByName(portal, 'portal_workflow')
        

        self.assertEqual((), workflow.getDefaultChain())


#    def test_view_permisison_for_self_roles(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('View' in [r['name'] for r in 
#                                portal.permissionsOfRole('Reader') if r['selected']])
#        self.assertTrue('View' in [r['name'] for r in 
#                                portal.permissionsOfRole('Knowledge Manager') if r['selected']])
#
#        self.assertTrue('View' in [r['name'] for r in 
#                                portal.permissionsOfRole('Maintenance Engineer') if r['selected']])
    
#    def test_staffmember_group_added(self):
#        portal = self.layer['portal']
#        acl_users = portal['acl_users']
#        
#        self.assertEqual(1, len(acl_users.searchGroups(name='Staff')))

#    def test_PloneFormGen_installed(self):
#        portal = self.layer['portal']
#        portal_types = getToolByName(portal, 'portal_types')
#        
#        self.assertTrue("FormFolder" in portal_types)
    
#    def test_forum_installed(self):
#        portal = self.layer['portal']
#        portal_types = getToolByName(portal, 'portal_types')
#        
#        self.assertTrue('eisoo.forum.forum' in portal_types)
#        
#    def test_km_installed(self):
#        portal = self.layer['portal']
#        portal_types = getToolByName(portal, 'portal_types')
#        
#        self.assertTrue('eisoo.km.faq' in portal_types)        
    
#    def test_metaTypesNotToList_configured(self):
#        portal = self.layer['portal']
#        portal_properties = getToolByName(portal, 'portal_properties')
#        navtree_properties = portal_properties['navtree_properties']
#        metaTypesNotToList = navtree_properties.getProperty('metaTypesNotToList')
#        
#        self.assertTrue("Promotion" in metaTypesNotToList)
#        self.assertTrue("Discussion Item" in metaTypesNotToList)
#        self.assertFalse("Cinema" in metaTypesNotToList)
    
    def test_add_thread_permission_for_member(self):
        portal = self.layer['portal']
        
        self.assertTrue('Eisoo: Add Thread' in [r['name'] for r in 
                                portal.permissionsOfRole('Member')
                                if r['selected']])
        self.assertFalse('Eisoo: End Thread' in [r['name'] for r in 
                                portal.permissionsOfRole('Member')
                                if r['selected']])        
        self.assertTrue('Eisoo: End Thread' in [r['name'] for r in 
                                portal.permissionsOfRole('Owner')
                                if r['selected']])
        self.assertTrue('Eisoo: Add Forum' in [r['name'] for r in 
                                portal.permissionsOfRole('Site Administrator')
                                if r['selected']])    
        self.assertFalse('Eisoo: Add Forum' in [r['name'] for r in 
                                portal.permissionsOfRole('Member')
                                if r['selected']])  
        self.assertTrue('Eisoo: Add Knowledge Base' in [r['name'] for r in 
                                portal.permissionsOfRole('Site Administrator')
                                if r['selected']])    
        self.assertFalse('Eisoo: Add Knowledge Base' in [r['name'] for r in 
                                portal.permissionsOfRole('Member')
                                if r['selected']]) 
#    def test_dam_report_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('dam-report' in portal_actions['site_actions'])
    
#    def test_contact_action_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('enquiry' in portal_actions['site_actions'])
#        self.assertFalse(portal_actions['site_actions']['contact'].visible)

    def test_manage_own_portlets_permission(self):
        portal = self.layer['portal']
        
#        self.assertTrue('Portlets: Manage own portlets' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('Maintenance Engineer')
#                        if r['selected']])
        self.assertTrue('Portlets: Manage own portlets' in
                [r['name'] for r in 
                    portal.permissionsOfRole('Member')
                        if r['selected']])
    
    def test_add_portal_member_permission(self):
        portal = self.layer['portal']
        
        self.assertTrue('Add portal member' in
                [r['name'] for r in 
                    portal.permissionsOfRole('Anonymous')
                    if r['selected']])
