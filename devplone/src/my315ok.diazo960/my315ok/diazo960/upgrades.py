from Products.CMFCore.utils import getToolByName
PROFILEID = 'profile-my315ok.diazo960:default'


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILEID)
