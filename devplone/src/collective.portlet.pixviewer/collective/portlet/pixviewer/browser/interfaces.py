   
from plone.theme.interfaces import IDefaultPloneLayer


from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

from zope.viewlet.interfaces import IViewletManager




class ISidebar(IViewletManager):
    """A viewlet manager that sits at the very top of the rendered page
    """
class ICompanyThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
class IMyNewBesideContent(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet beside the main content.
    """  
class IMyNewAboveContentView(IPortletManager,IColumn):
    """we need our own portlet manager for loading viewlet above the content area.
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
    
