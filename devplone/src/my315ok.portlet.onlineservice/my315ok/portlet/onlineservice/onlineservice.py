# -*- coding: utf-8 -*-
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from my315ok.portlet.onlineservice import OnlineServiceMessageFactory as _


class IOnlineService(IPortletDataProvider):
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
    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)
    sitename = schema.TextLine(title=_(u"site name"),
                             description=_(u"name of the web site"),
                             required=True)
    mailaddr = schema.TextLine(title=_(u"mail address"),
                             description=_(u"mail address"),
                             required=True)
    qqnumber = schema.Int(title=_(u"number"),
                       description=_(u"Specify the tencenter qq number that provided customer service."),
                       required=True)
    qqnumber2 = schema.Int(title=_(u"second number"),
                       description=_(u"Specify the second qq number that provided customer service.")
                       )
    telnumber = schema.Int(title=_(u"phone"),
                       description=_(u"Specify the telphone number that provided customer service."),
                       required=True)
    
    cssid = schema.TextLine(title=_(u"css id"),
                             description=_(u"css id of the float qq portlet"),
                             required=True)
    xpos = schema.Int(title=_(u"x position"),
                       description=_(u"Specify start x position of the qq float portlet."),
                       required=True)
    ypos = schema.Int(title=_(u"y position"),
                       description=_(u"Specify start y position of the qq float portlet."),
                       required=True)

    


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IOnlineService)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""
    header = u""
    sitename= u""
    mailaddr= u""
    cssid = ""    
    xpos = None
    ypos = None
    qqnumber = None
    qqnumber2 = None
    telnumber = None

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self,header=u"",sitename=u"",qqnumber2=None,mailaddr=u"",telnumber=None,cssid="",xpos=None,ypos=None,qqnumber=None):
        
        self.qqnumber = qqnumber
        self.sitename = sitename      
        self.cssid = cssid
        self.xpos = xpos
        self.ypos = ypos
        self.qqnumber2 = qqnumber2
        self.header = header
        self.telnumber = telnumber
        self.mailaddr = mailaddr

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

    render = ViewPageTemplateFile('onlineservice.pt')
    def available(self):
        if len(self.data.qqnumber) > 0:
            return 1
        else:
            return 0


    def qq_js(self):
        out = """
        function CloseQQ(){jq("#%s").css("display","none")}jq(this).scroll(function(){var bodyTop=0;if(typeof window.pageYOffset!='undefined'){bodyTop=window.pageYOffset}else if(typeof document.compatMode!='undefined'&&document.compatMode!='BackCompat'){bodyTop=document.documentElement.scrollTop}else if(typeof document.body!='undefined'){bodyTop=document.body.scrollTop}jq("#%s").css("top",%s+bodyTop);jq("#%s").css("left",%s)});
        """ % (self.data.cssid,self.data.cssid,self.data.ypos,self.data.cssid,self.data.xpos)
        return out
    def parameters(self):
        data = self.data
        href="tencent://message/?uin=%s&Site=%s&Menu=yes" % (data.qqnumber,data.sitename)
        return href
    def qqsupporter(self):
        data = self.data
        if data.qqnumber2 != None:
            href="tencent://message/?uin=%s&Site=%s&Menu=yes" % (data.qqnumber2,data.sitename)
            return href
        else:
            return self.parameters()
            
    def maillink(self):
        data = self.data
        href="mailto:%s?subject=%s site mail" % (data.mailaddr,data.sitename)
        return href 
    def mailcontent(self):
        content = str(self.data.mailaddr)
        if len(content) > 10:
            con ="发送邮件"
#            con =_(u"send mail")
        else:
            con = content.replace('@', 'at')                       
        return con     


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IOnlineService)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IOnlineService)
    
##function CloseQQ(){jq("#%s").css("display","none")}jq(this).scroll(function(){var bodyTop=0;if(typeof window.pageYOffset!='undefined'){bodyTop=window.pageYOffset}else if(typeof document.compatMode!='undefined'&&document.compatMode!='BackCompat'){bodyTop=document.documentElement.scrollTop}else if(typeof document.body!='undefined'){bodyTop=document.body.scrollTop}jq("#%s").css("top",%s+bodyTop);jq("#%s").css("left",%s)});
out2 = """
        function CloseQQ(){jq("#%s").css("display","none");}
        jq(this).scroll(function() {   
    var bodyTop = 0;    
    if (typeof window.pageYOffset != 'undefined') {    
      bodyTop = window.pageYOffset;    
    }
    else if (typeof document.compatMode != 'undefined' && document.compatMode != 'BackCompat')
    {    
      bodyTop = document.documentElement.scrollTop;    
    }    
    else if (typeof document.body != 'undefined') {    
      bodyTop = document.body.scrollTop;    
    }  
    jq("#%s").css("top", %s + bodyTop); 
     jq("#%s").css("left", %s);            
});
        """    
