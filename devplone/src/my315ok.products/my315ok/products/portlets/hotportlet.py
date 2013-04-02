from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from Products.ATContentTypes.interface import IATTopic

from plone.portlet.collection import PloneMessageFactory as _a

from my315ok.products import MessageFactory as _

class IHotPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)
    header = schema.TextLine(title=_a(u"Portlet header"),
                             description=_a(u"Title of the rendered portlet"),
                             required=True)
    target_collection = schema.Choice(title=_a(u"Target collection"),
                                  description=_a(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : IATTopic.__identifier__},
                                                                    default_query='path:'))
    limit = schema.Int(title=_a(u"Limit"),
                       description=_a(u"Specify the maximum number of items to show in the portlet. "
                                       "Leave this blank to show all items."),
                       required=False)
    rows = schema.Int(title=_a(u"rows"),
                       description=_a(u"Specify the rows number."),
                       required=False)
    cols = schema.Int(title=_a(u"cols"),
                       description=_a(u"Specify the cols number."),
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
        vocabulary = 'product.ImageSizeVocabulary' )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IHotPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u"):
    #    self.some_field = some_field
    header = u""
    target_collection = None
    limit = 5
    rows = 1
    cols = 1
    show_more = True
    previewmode = u"thumb"

    def __init__(self, header=u"", target_collection=None, limit=None,rows=1,cols=1,show_more=True, previewmode=u"thumb"):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.rows = rows
        self.cols = cols
        self.show_more = show_more
        self.previewmode = previewmode

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "hot_portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('hotportlet.pt')   

    @property
    def available(self):
        return len(self.results())

    def rows(self):       
        return self.data.rows
        
    def cols(self):
        return self.data.cols
    
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
    def parentobjurl(self,obj):
        parent = obj.aq_inner.aq_parent
        return parent.absolute_url()
    
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
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.unrestrictedTraverse(collection_path, default=None)
    
    @memoize   
    def main_parameters(self):
        """ fetch product parameters"""              
        brains = self.results()
        sc = self.data.previewmode
        goods = []           
        for bs in brains:
# bs is a brain of the object that is implemented Iproductfolder             
            if bs.portal_type != "multiproducts":
                continue               
            tmp = self.add_paras(bs,sc)
            goods.append(tmp)
        return goods
    
    # here is set local varible item avoid by overed.
    def add_paras(self,bn,scale):
        """given a multiproducts brain,fetch products parameters"""

        item={}
        item['title'] =  self.get_goods_img(bn,scale)['title']        
        item['photo'] = self.get_goods_img(bn,scale)['tag']
        item['img_url'] =  self.get_goods_img(bn,scale)['url']        
        item['goods_url'] = bn.getURL()
        return item
                      
    @memoize
    def get_goods_img(self,obj,scale):

        catalog = getToolByName(self.context, 'portal_catalog')
        sepath =  obj.getPath() 
        query = {'meta_type':('product'),
                 'sort_on':'getObjPositionInParent',
                 'sort_order':'forward',
                 'path':sepath,
                 }        
        sd = catalog(query)
# fetch first product in product folder        
        mainimgbn = sd[0]
        tl = mainimgbn.Title
        base = mainimgbn.getURL()
        url = base + "/image_" + scale
        imgtag ="<img src ='%s' alt='%S'/>" % (url,tl)
        img_info = {}
        img_info['tag']= imgtag
        img_info['title']= tl
        img_info['url']= base
        return img_info 


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IHotPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IHotPortlet)
