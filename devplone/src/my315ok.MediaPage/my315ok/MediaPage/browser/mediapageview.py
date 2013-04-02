from zope.interface import implements, Interface

from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from my315ok.MediaPage import MediaPageMessageFactory as _
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ImediapageView(Interface):
    """
    mediapage view interface
    """

    def test(a,b,c):
        """ test method,if a as 'True',return b ,else return c"""

class mediapageView(BrowserView):
    """
    mediapage browser view
    """
    implements(ImediapageView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self,**kw):

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog.searchResults(**kw)

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @memoize
    def results(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        sepath= '/'.join(context.getPhysicalPath()) 
#        catalog = getToolByName(self.context, 'portal_catalog')        
#        sepath = '/'.join(self.context.getPhysicalPath()) 
        query = {'meta_type':('rich_image'),
                 'sort_on':'getObjPositionInParent',
                 'sort_order':'forward',
                 'path':sepath,
		 'level':1,
                 }
        
        sd = catalog(query)
        return sd

    def test(self,a,b,c):
        if a:
            return b
        else:
            return c
        
    @memoize
    def allimages(self):
        allobject = map(lambda b: b.getObject(),self.results())
        return allobject
    def UseImageZoom(self):
        return self.context.getUseImageZoom()
    def Displaymodel(self):
        return self.context.getDisplaymodel()
    def PerPagePrdtNum(self):
        return self.context.getPerPagePrdtNum()
    def PerRowPrdtNum(self):
        return self.context.getPerRowPrdtNum()
    def AutoChangeDelay(self):
        return self.context.getAutoChangeDelay()
    def AutoChangeRandom(self):
        return self.context.getAutoChangeRandom()
    

    @memoize
    def createAutoImagesJSCode(self):
##        import pdb
##        pdb.set_trace()
        jsOut = ''
        imgList = self.allimages()
        if self.context.getUseImageZoom():
            useZoom = 1
        else:
            useZoom = 0
            
        if not imgList:
            return {'jsCode': '', 'firstImage': None}

        autoChangeDelay = self.AutoChangeDelay()
        useRandom       = self.AutoChangeRandom()

        # randomize image list
        if useRandom:
            # randomize list
            shuffle(imgList)

        # create the JS code sequence
        if imgList:
            jsOut  += 'var allImages = new Array();\n'
            jsOut  += 'var allImageTitle = new Array();\n'
            idx     = 0
            for img in imgList:
                jsOut += 'allImages[%s] = new Image();\n' % str(idx)
                jsOut += 'allImages[%s].src = "%s/image_preview";\n' %(str(idx),img.absolute_url())
                jsOut += 'allImageTitle[%s] = "%s";\n' %(str(idx),img.Title())
                idx += 1

            jsOut += """                    
                    var autoChangeDelay = %(autoDelay)s;initAutoChange();var imgNum = 0;var useZoom = %(ifZoom)s;           
                    """ % dict(autoDelay=autoChangeDelay, ifZoom=useZoom)
        
        return {'jsCode': jsOut, 'firstImage': imgList[0]}

