from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter
from Acquisition import aq_inner

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.ATContentTypes.interface import IATFile, IATImage


from collective.portlet.pixviewer import PixviewerPortletMessageFactory as _
from plone.portlet.collection import PloneMessageFactory as _a

from Products.CMFCore.utils import getToolByName

class IVideoPortlet(IPortletDataProvider):
    """A portlet which can display videos
    """

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)
    swfsrc = schema.TextLine(title=_(u"target URI"),
                             description=_(u"the URI of the video,accept http://a.b.com/s.flv format"),
                             required=False)

    target = schema.Choice(title=_(u"Target object"),
                           description=_(u"This can be a file containing an FLV file, or a folder or collection containing FLV files"),
                           required=False,
                           source=SearchableTextSourceBinder({'object_provides' :IATFile.__identifier__},
                                                               default_query='path:'))
    locid = schema.TextLine(title=_(u"video id"),
                             description=_(u"the video player's position will put"),
                             required=False,
                             default=u"player")
    
    show_more = schema.Bool(title=_a(u"Show more... link"),
                       description=_a(u"If enabled, a more... link will appear in the footer of the portlet, "
                                      "linking to the underlying Collection."),
                       required=True,
                       default=True)
    style = schema.TextLine(title=_(u"css style"),
                             description=_(u"the css inline style of the video player zone"),
                             default=u"display:block;width:520px;height:330px",
                             required=True)
                                                               
    splash = schema.Choice(title=_(u"Splash image"),
                           description=_(u"An image file to use as a splash image"),
                           required=False,
                           source=SearchableTextSourceBinder({'object_provides' : IATImage.__identifier__},
                                                               default_query='path:'))

class Assignment(base.Assignment):
    implements(IVideoPortlet)

    header = u""
    swfsrc = u""
    target = None
    locid = u"player"
    splash = None
    show_more = None
    style = None

    def __init__(self, header=u"",swfsrc=u"", target=None,locid=u"player",show_more=None,style=None, splash=None):
        self.header = header
        self.swfsrc = swfsrc
        self.target = target
        self.locid = locid
        self.show_more = show_more
        self.style = style
        self.splash = splash

    @property
    def title(self):
        return self.header

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('flashplayerportlet.pt')

    @property
    def available(self):
        return (self.target_url() ==None)

    def target_url(self):
        videourl = self.data.swfsrc
        if videourl:
            return videourl
        
        target = self.target()
        if target is None:
            return None
        else:
            return target.absolute_url()
    
    def portal(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal
    
    @memoize
    def splash(self):
        splash_path = self.data.splash
        if not splash_path:
            return None
        if splash_path.startswith('/'):
            splash_path = splash_path[1:]        
        if not splash_path:
            return None
        portal = self.portal()
        splash = portal.unrestrictedTraverse(splash_path, default=None)        
        if splash is not None and not IATImage.providedBy(splash):
            return None        
        return splash

    def player_css(self):
        css = self.data.style
        return css
            
    @memoize
    def target(self):
        target_path = self.data.target
        if not target_path:
            return None

        if target_path.startswith('/'):
            target_path = target_path[1:]
        
        if not target_path:
            return None       
        portal = self.portal()
        return portal.unrestrictedTraverse(target_path, default=None)
    
    @memoize
    def js_settings(self):
#        import pdb
#        pdb.set_trace()
        player = self.data.locid
        if player == None:
            player = u"player"
        out = """jq(document).ready(function(){
         flowplayer("%(swfile)s","http://releases.flowplayer.org/swf/flowplayer-3.2.5.swf",
         {plugins:{pseudo: {url:'flowplayer.pseudostreaming-3.2.5.swf'}}});});""" % dict(swfile=player)
        return out
           
        
class AddForm(base.AddForm):
    form_fields = form.Fields(IVideoPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget
    form_fields['splash'].custom_widget = UberSelectionWidget
    
    label = _(u"Add Video Portlet")
    description = _(u"This portlet display a Flash Video")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IVideoPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget
    form_fields['splash'].custom_widget = UberSelectionWidget

    label = _(u"Edit Video Portlet")
    description = _(u"This portlet display a Flash video.")
