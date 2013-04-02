# -*- coding: utf-8 -*-
import re
from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.ATContentTypes.interface import IATTopic
from collective.portlet.pixviewer import PixviewerPortletMessageFactory as _
from plone.portlet.collection import PloneMessageFactory as _a
color_validator = re.compile("[a-fA-F\d]{6,6}$").match

class IPixviewerPortlet(IPortletDataProvider):
    """A portlet
    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
   
    header = schema.TextLine(title=_a(u"Portlet header"),
                             description=_a(u"Title of the rendered portlet"),
                             required=True)

    target_collection = schema.Choice(title=_a(u"Target collection"),
                                  description=_a(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : IATTopic.__identifier__},
                                                                    default_query='path:'))
    local_id = schema.TextLine(title=_(u"video id"),
                             description=_(u"the video player's position will put"),
                             required=False,
                             default=u"switchpics_id")

    limit = schema.Int(title=_a(u"Limit"),
                       description=_a(u"Specify the maximum number of items to show in the portlet. "
                                       "Leave this blank to show all items."),
                       required=False)
    show_more = schema.Bool(title=_a(u"Show more... link"),
                       description=_a(u"If enabled, a more... link will appear in the footer of the portlet, "
                                      "linking to the underlying Collection."),
                       required=True,
                       default=True)

    previewmode = schema.Choice(
        title=_(u"image size"),
        description=_(u"Choose source image size"),
        required = True,
        default = "thumb",
        vocabulary = 'pixviewer.ImageSizeVocabulary' )

    focus_width = schema.Int(title=_(u"focus_width"),
                       description=_(u"Specify the width of focused image."),                                      
                       required=True)
    focus_height = schema.Int(title=_(u"focus_height"),
                       description=_(u"Specify the height of focused image."),
                       required=True)
    swf_width = schema.Int(title=_(u"swf_width"),
                       description=_(u"Specify the width of the full flash."),
                       required=True)
    swf_height = schema.Int(title=_(u"swf_height"),
                       description=_(u"Specify the height of the full flash."),
                       required=True)
    text_height = schema.Int(title=_(u"text_height"),
                       description=_(u"Specify the height of focused text."),
                       required=True)
    color_bg = schema.TextLine(
        title=_(u"Background color"),
        description=_(u"Choose a custom background color. Use hex color codes."),
        required=True,
        default=u"ffffff",
        constraint=color_validator)

class Assignment(base.Assignment):
    """Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IPixviewerPortlet)
    header = u""
    target_collection = None
    local_id = u"switchpics_id"
    limit = 5
    show_more = True
    previewmode = u"thumb"
    focus_width = None
    focus_height = None
    swf_width = None
    swf_height = None
    text_height = None
    color_bg =u"ffffff"
    
    def __init__(self, header=u"", target_collection=None, local_id=u"switchpics_id",limit=None, show_more=True, previewmode=u"thumb", focus_width=None,
    focus_height=None,
    swf_width=None,
    swf_height=None,
    text_height=None,
    color_bg=u"ffffff"):
        self.header = header
        self.target_collection = target_collection
        self.local_id = local_id
        self.limit = limit
        self.show_more = show_more
        self.previewmode = previewmode
        self.focus_width = focus_width
        self.focus_height = focus_height
        self.swf_width = swf_width
        self.swf_height = swf_height
        self.text_height = text_height
        self.color_bg = color_bg

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('pixviewerportlet.pt')
    @property
    def available(self):
        return len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def results(self):
        """ Get the actual result brains from the collection. 
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""
        
        return self._standard_results()

    @memoize
    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog()
            if self.data.limit and self.data.limit > 0:
                results = results[:self.data.limit]
        return results         
        
    @memoize
    def collection(self):
        """ get the collection the portlet is pointing to"""
        
        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]
        
        if not collection_path:
            return None
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.unrestrictedTraverse(collection_path, default=None)

    @memoize
    def js_settings(self):
##        import pdb
##        pdb.set_trace()
        data = self.data
        out =  []
        out.append('<!--')
        out.append('var focus_width = %s;' %data.focus_width)
        out.append('var focus_height = %s;' %data.focus_height)
        out.append('var text_height = %s;' %data.text_height)              
        out.append('var swf_height = %s;' %data.swf_height)
        out.append('var swf_height_str = "%s";' %data.swf_height) 
        out.append('var swf_width = %s;' %data.swf_width)
        out.append('var swf_width_str = "%s";' %data.swf_width)
        out.append('var color_bg = "%s";' %data.color_bg)
        out.append('var locid = "%s";' %data.local_id)
#        out.append('var swfurl="/++resource++collective.portlet.pixviewer.swf/pixviewer.swf";')        
        out.append('var swfurl="http://images.315ok.org/pixviewer.swf";')
        pics=''
        links=''
        texts=''
              
        if self.results():
            pass
        else:
            return "document.write('Can not found images!');"
        mode = data.previewmode
        if mode == "orig":
            for obj in self.results():
                baseurl = obj.getURL()
                tl = obj.Title
                pics += baseurl + '/image|'
                links += baseurl + '|'
                texts += tl + '|'

            picst = pics[:-1]
            linkst = links[:-1]
            textst = texts[:-1]
            out.append('var pics = "'+picst+'";')              
            out.append('var links = "'+linkst+'";')   
            out.append('var texts = "'+textst+'";')
            
        else:            
            for obj in self.results():
                baseurl = obj.getURL()
                tl = obj.Title
                pics += baseurl + '/image_%s|' %data.previewmode
                links += baseurl + '|'
                texts += tl + '|'

            picst = pics[:-1]
            linkst = links[:-1]
            textst = texts[:-1]
            out.append('var pics = "'+picst+'";')              
            out.append('var links = "'+linkst+'";')   
            out.append('var texts = "'+textst+'";')                  

        out.append('<!--')
        out.append('var fo = new FlashObject(swfurl,locid,swf_width_str,swf_height_str,"6",color_bg);')
        out.append('fo.addParam("menu","false");')
        out.append('fo.addVariable("pics", pics);')
        out.append('fo.addVariable("links", links);')
        out.append('fo.addVariable("texts", texts);')
        out.append('fo.addVariable("borderwidth",focus_width);')
        out.append('fo.addVariable("borderheight",focus_height);')
        out.append('fo.addVariable("textheight",text_height);') 
        out.append('fo.addVariable("curhref","http://315ok.org/");')   
        out.append('fo.addParam("quality","best");')
        out.append('fo.addParam("scale","noscale");')
        out.append('fo.addParam("wmode", "opaque");') 
        out.append('fo.addParam("height", swf_height);')
        out.append('fo.addParam("width", swf_width);')
        out.append('fo.addParam("allowScriptAccess","sameDomain");')
        out.append('fo.write(locid);')
        out.append('-->')
        return u'\n'.join(out)

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IPixviewerPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    
    label = _a(u"Add Collection Portlet")
    description = _a(u"This portlet display a listing of items from a Collection.")

    def create(self, data):
        return Assignment(**data)
    

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPixviewerPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _a(u"Edit Collection Portlet")
    description = _a(u"This portlet display a listing of items from a Collection.")
