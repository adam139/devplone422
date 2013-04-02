from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from Products.CMFPlone.browser.interfaces import ISitemapView

from zope.interface import Interface

class Iorgimgview(Interface):
    """A viewlet manager that sits at the very top of the rendered page
    """
class ImagesView(BrowserView):
    implements(Iorgimgview)

    def imgrollMap(self):
#        context = aq_inner(self.context)
#        request = self.request       
       
        return  """<html>
<head><link url="" /><title text="sdsdsd"> </title><link url="" /><title text="sdsdsd5"> </title><link url="" /><title text="sdsdsd56"> </title></head>
<body>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll1.png" alt="sdsdsd" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll2.png" alt="sdsdsd5" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll3.png" alt="sdsdsd56" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll1.png" alt="sdsdsd" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll2.png" alt="sdsdsd5" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/roll3.png" alt="sdsdsd56" /></a></div>
</body>
</html>

       """
    def imgsliderMap(self):
#        context = aq_inner(self.context)
#        request = self.request       
       
        return  """<html>
<head><link url="" /><title text="sdsdsd"> </title><link url="" /><title text="sdsdsd5"> </title><link url="" /><title text="sdsdsd56"> </title></head>
<body>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/slider1.png" alt="slider" /></a></div>
<div class="banner"><a href=""><img src="++resource++my315ok.companytheme.images/slider2.jpg" alt="slider2" /></a></div>
</body>
</html>

       """
        