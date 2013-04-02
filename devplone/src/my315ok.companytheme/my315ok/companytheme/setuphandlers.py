def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('my315ok.companytheme_various.txt') is None:
        return

    # Add additional setup code here
    def updateCatalog(context, clear=True):
        portal = context.getSite()
        logger = context.getLogger('my315ok.companytheme updateCatalog')
        logger.info('Updating catalog (with clear=%s) so items in profiles/default/structure are indexed...' % clear )
        catalog = portal.portal_catalog
        err = catalog.refreshCatalog(clear=clear)
        if not err:
            logger.info('...done.')
        else:
            logger.warn('Could not update catalog.')

