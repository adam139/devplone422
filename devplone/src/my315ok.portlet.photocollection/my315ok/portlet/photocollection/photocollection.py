from zope.interface import implements
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from my315ok.portlet.photocollection import photocollectionMessageFactory as _ 


from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from plone.portlet.collection.collection import ICollectionPortlet
from plone.portlet.collection.collection import Assignment as baseAssignment
from plone.portlet.collection.collection import Renderer as baseRenderer


# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
#from my315ok.portlet.photocollection import photocollectionMessageFactory as _


class Iphotocollection(ICollectionPortlet):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    crop_title = schema.Bool(title=_(u"crop title"),
                         description=_(u"If enabled, title will be cropped using specify number words."),
                         required=True,
                         default=False)
    wordsnum = schema.Int(title=_(u"number"),
                       description=_(u"Specify the maximum number of words to show as title. "
                                       "Leave this blank to show all items."),
                       default=75,
                       required=False)

class Assignment(baseAssignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(Iphotocollection)

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False, 
                 crop_title=1,wordsnum=75):
        super(Assignment,self).__init__(header, target_collection, limit, 
                                        random, show_more, show_dates)
        self.crop_title = crop_title
        self.wordsnum = wordsnum

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"photocollection")


class Renderer(baseRenderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('photocollection.pt')
    
    def getImage(self,obj,scale="mini"):
#        import pdb
#        pdb.set_trace()
        url = obj.getURL()
        imgurl = url + "/image_" + scale
#        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
#        portal = portal_state.portal()
#        tmp = portal.unrestrictedTraverse(imgurl, default=None)
#        if tmp ==None:        
#            return ""
#        else:
        return imgurl
    
    def cropTitle(self,text, length, ellipsis='...'):
        if length == 0 or length == None:
            return text
        context = aq_inner(self.context)
        pview = getMultiAdapter((context,self.request),name=u"plone")
#        pview = getMultiAdapter((self.parent(), self.request), name=u'earthqk_event_view')
        croped = pview.cropText(text, length)
        return croped
    
    def goodtext(self,brain):
        len = self.data.wordsnum
        des = brain.Description
        ttl = brain.Title
        if des == None:
            return self.cropTitle(ttl, len)
        else:
            return self.cropTitle(des, len)                      


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(Iphotocollection)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(Iphotocollection)
