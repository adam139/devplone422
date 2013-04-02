from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from my315ok.portlet.embediframe import EmbedIframePortletMessageFactory as _
from plone.portlet.collection import PloneMessageFactory as _a

from plone.memoize.instance import memoize

class IEmbedIframePortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    header = schema.TextLine(title=_a(u"Portlet header"),
                             description=_a(u"Title of the rendered portlet"),
                             required=True)
    framesrc = schema.URI(title=_(u"target URI"),
                             description=_(u"the URI of target frame "),
                             required=True)
    height = schema.TextLine(title=_(u"iframe height"),
                             description=_(u"height of the rendered iframe"),
                             required=True)
    width = schema.TextLine(title=_(u"iframe width"),
                             description=_(u"width of the rendered iframe"),
                             required=True)
    style = schema.TextLine(title=_(u"css style"),
                             description=_(u"the css inline style of the iframe tag"),
                             required=True)
    frameborder = schema.Bool(title=_(u"border"),
                             description=_(u"if this iframe has border"),
                             required=True,
                              default=False)
    scrolling = schema.Choice(title=_(u"scrolling"),
                             description=_(u"if this iframe can scroll"),
                             required=True,
                              vocabulary = 'embediframeportlet.ScrollingVocabulary')  


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IEmbedIframePortlet)
    header = u""
    framesrc = None
    height = None
    width = None
    style = None
    frameborder = False
    scrolling = "auto"   

    def __init__(self,header=None,framesrc=None,height=None,width=None,style=None,frameborder=False,scrolling="auto"):

        self.header = header
        self.framesrc = framesrc
        self.height = height
        self.width = width
        self.style = style
        self.frameborder = frameborder
        self.scrolling = scrolling
        

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return  self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('embediframeportlet.pt')

    @property
    def available(self):
        import urllib2
        opener = urllib2.build_opener()
        try:
            f = opener.open("%s" % self.data.framesrc)
#            temp = f.read()
#            f.close()
            return True
        except:
            return False          
                    

    @memoize
    def results(self):
        """ Get the actual result brains from the collection. 
            This is a wrapper so that we can memoize if and only if we aren't
            selecting random items."""            
    
        out=''
        if self.data.frameborder:
            isborder = 1
        else:
            isborder = 0
        if self.available:
            out = '<iframe src="%s" width="%s" height="%s" style="%s" frameborder="%s" scrolling="%s">' \
            % (self.data.framesrc,self.data.width,self.data.height,self.data.style,isborder,self.data.scrolling)
            out += '<p>your browser can not support ifame</p></iframe>'
        return out     

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IEmbedIframePortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IEmbedIframePortlet)
