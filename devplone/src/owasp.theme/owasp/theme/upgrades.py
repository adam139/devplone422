from Products.CMFCore.utils import getToolByName
PROFILEID = 'profile-owasp.theme:default'


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILEID)
