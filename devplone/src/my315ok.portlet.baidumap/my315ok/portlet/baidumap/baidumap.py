#-*- coding: UTF-8 -*-
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

# TODO: If you define any fields for the portlet configuration schema below
# do not forget to uncomment the following import
from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# TODO: If you require i18n translation for any of your schema fields below,
# uncomment the following to import your package MessageFactory
from my315ok.portlet.baidumap import baidumapMessageFactory as _


class Ibaidumap(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)
    mapcontainerid = schema.TextLine(title=_(u"id"),
                       description=_(u"a Div id of the map container"),
                        required=True
                      )  
    level = schema.Int(title=_(u"level"),
                       description=_(u"Specify a level for the baidu map."),
                       default=12,
                       required=True) 
    
    label = schema.TextLine(title=_(u"label"),
                             description=_(u"the label for map marker"),
                             required=True)
    
    offsetx = schema.Int(title=_(u"x"),
                       description=_(u"Specify a x offset"),
                       default=12,
                       required=True) 
    
    offsety = schema.Int(title=_(u"y"),
                       description=_(u"Specify a y offset"),
                       default=12,
                       required=True)         
        
        
    longitude = schema.Float(title=_(u"Longitude"),
                       description=_(u"Specify longitude of the given position,using float."),
                       default=112.9178,
                       required=True) 
    latitude = schema.Float(title=_(u"Latitude"),
                       description=_(u"Specify latitude of the given position,using float."),
                       default=27.8368,
                       required=True)           

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(Ibaidumap)

    # TODO: Set default values for the configurable parameters here

    header = u""
    mapcontainerid = u"mapcontainer"
    level =12
    label=u""
    offsetx = 20
    offsety = -10
    longitude = 112.9178
    latitude = 27.8368

 #    TODO: Add keyword parameters for configurable parameters here
    def __init__(self, header=u"",mapcontainerid=u"mapcontainer",level=12,label=u"",\
                 offsetx=20,offsety=-10,longitude=112.9178,latitude=27.8368):
        self.header = header
        self.mapcontainerid = mapcontainerid
        self.level = level
        self.label = label
        self.offsetx = offsetx
        self.offsety = offsety
        self.longitude = longitude
        self.latitude = latitude                                                        


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

    render = ViewPageTemplateFile('baidumap.pt')
    out = """
    <!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
body, html,#allmap {width: 100%;height: 100%;overflow: hidden;margin:0;}
#l-map{height:100%;width:78%;float:left;border-right:2px solid #bcbcbc;}
#r-result{height:100%;width:20%;float:left;}
</style>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=1.4"></script>
<title>带文字标签的覆盖物</title>
</head>
<body>
<div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
var map = new BMap.Map("allmap");
var point = new BMap.Point(116.400244,39.92556);
map.centerAndZoom(point, 12);
var marker = new BMap.Marker(point);  // 创建标注
map.addOverlay(marker);              // 将标注添加到地图中

var label = new BMap.Label("我是文字标注哦",{offset:new BMap.Size(20,-10)});
marker.setLabel(label);
var map = new BMap.Map("mapcontainer");
var point = new BMap.Point(112.9178,27.8368);
map.centerAndZoom(point, 12);
var marker = new BMap.Marker(point);
map.addOverlay(marker);
var label = new BMap.Label("yiyuan",{offset:new BMap.Size(12,12)});
marker.setLabel(label);
</script>

    """
    def jscode(self):
        data = self.data
        mapcontainerid = data.mapcontainerid
        longitude = data.longitude
        latitude = data.latitude
        level = data.level
        label = data.label
        offsetx = data.offsetx
        offsety = data.offsety
        
        jscode="""var map = new BMap.Map("%(containerid)s");
var point = new BMap.Point(%(longitude)s,%(latitude)s);
map.centerAndZoom(point, %(level)s);
var marker = new BMap.Marker(point);  
map.addOverlay(marker);              

var label = new BMap.Label("%(label)s",{offset:new BMap.Size(%(x)s,%(y)s)});
marker.setLabel(label);""" % dict(containerid=mapcontainerid,longitude=longitude,latitude=latitude,level=level,label=label,x=offsetx,y=offsety)

        return jscode



class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(Ibaidumap)

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
    form_fields = form.Fields(Ibaidumap)
