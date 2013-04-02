from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

from zope.viewlet.interfaces import IViewletManager

from zope.interface import Interface

class IThemeSpecific(Interface):
    """Marker interface that defines a ZTK browser layer. We can reference
    this in the 'layer' attribute of ZCML <browser:* /> directives to ensure
    the relevant registration only takes effect when this theme is installed.
    
    The browser layer is installed via the browserlayer.xml GenericSetup
    import step.
    """
class ISunburstView(Interface):
    """ """

    def getColumnsClass():
        """ Returns the CSS class based on columns presence. """





class ISidebar(IViewletManager):
    """A viewlet manager that sits at the outerest of the rendered page
    """

class IMyNewBesideContent(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet beside the main content.
    """  
    
class IMyNewLoginContent(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet login the main content.
    """  
class IMyNewAboveContentView(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet above the content view area.
    """

class IMyNewAboveContent(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet above the content area.
    """
class IMyNewBelowContent(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet below the content area.
    """    

class IMyFooterPortalFooter(IPortletManager,IColumn):
    """we need our own footerzone portlet manager for loading viewlet above the footer area.
    """

class IMyNewPortalHeader(IPortletManager,IColumn):
    """we need our own roll zone portlet manager for loading viewlet below the global section area.
    """
class IMyLogoPortalHeader(IPortletManager,IColumn):
    """we need our own logo portlet manager for loading my logoviewlet and it usually is above the global section area.
    """
    