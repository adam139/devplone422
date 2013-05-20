#-*- coding: UTF-8 -*-
from five import grok
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from my315ok.products.productfolder import Iproductfolder
from my315ok.products.product import Iproduct
from plone.memoize.instance import memoize
from BeautifulSoup import BeautifulSoup as bt

class baseview(grok.View):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('view')

#<img src="" tal:attributes="src string:${item/getURL}/@@images/image/thumb" />

    def fetch_list_position(self,lt,item):
        if item in lt:
            for i in range(len(lt)):
                if lt[i] == item:
                    break
                else:
                    continue
            return i
        else:
            return 0                
        
    @property
    def PerPagePrdtNum(self):
        return self.context.PerPagePrdtNum  
        
    @property
    def PerRowPrdtNum(self):
        return self.context.PerRowPrdtNum 
    
    def span_num(self):
#        import pdb
#        pdb.set_trace()
        return "span" + str(12/self.PerRowPrdtNum)
         
    @memoize
    def prdt_images(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        sepath= '/'.join(self.context.getPhysicalPath()) 
        query = {'object_provides': Iproduct.__identifier__,
                 'review_status':'published',
                 'sort_on':'getObjPositionInParent',
                 'sort_order':'forward',
                 'path':sepath,
                 }        
        sd = catalog(query)
        return sd    

    @memoize
    def img_fast_tag(self,fieldname="image",small="tile",preview="mini",large="large"):

        imglists = {}
        csmall = []
        cpreview = []
        clargelink = []
        imgviewurl = []
        imgtitle = []
        imgcaption = []        
           
        for i in self.prdt_images():            
                try:
                    objurl = i.getURL()
                    base =  objurl + "/@@images/" + fieldname + "/"
                    tl = i.Title
                    caption = i.Description
                    surl = base  + small
                    purl = base  + preview
                    lurl = base  + large 
                    simg = "<img src='%s' alt='%s' />" % (surl,tl)
                    pimg = "<img src='%s' alt='%s' />" % (purl,tl)
#<img src="" tal:attributes="src string:${item/getURL}/@@images/image/thumb" />                    
#                    limg = "<img src='%s' alt='%s' title='%s' />" % (lurl,tl,tl)
                    imgobjurl = objurl + "/@@view"                    
                    csmall.append(simg)
                    cpreview.append(pimg)
                    clargelink.append(lurl)
                    imgviewurl.append(imgobjurl)
                    imgtitle.append(tl)
                    imgcaption.append(caption)
                except:
                    continue            
        imglists["small"] = csmall
        imglists["preview"] = cpreview
        imglists["large"] = clargelink
        imglists["imgurl"] = imgviewurl
        imglists["title"] = imgtitle
        imglists["caption"] = imgcaption        
        return imglists
    
    def mainimage(self,fieldname="image"):
        main = self.img_fast_tag("image")
        return main
    
# bt is beautiful soup ,small picture come from rich text field's img tag      
    def auximage(self,j):
        aux = self.details(fieldname="text")
        sp = bt(aux["comments"][j])
        try:
            auim = sp("img")[0].__str__()
        except:
            auim = ""
        return auim
# if table exist then return parameter table        
    def parameters(self,j):
        aux = self.details(fieldname="text")
        sp = bt(aux["comments"][j])
       
        try:
            par = sp("table")[0].__str__()
        except:
            par = ""
        return par
# overview
    def overview(self,j):
#        import pdb
#        pdb.set_trace()
        return  self.details(fieldname="text")['comments'][j]
    
 # fetch product footer notes   
    def notes(self,j):
        aux = self.details(fieldname="text")
        sp = bt(aux["comments"][j])
       
        try:
            par = sp.find("div","footer-notes")
            if par ==None:
                par = ""
            else:
                par = par.__str__()
        except:
            par = ""
        return par        
        
    @memoize
    def details(self,fieldname="text"):
        imglists = {}         
        cpara = [i.text for i in self.prdt_images()]                         
        imglists["comments"] = cpara        
        return imglists
    
    def test(self,a,b,c):
        if a:
            return b
        else:
            return c    


class mediapageview(baseview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('mediapageview')
    
    def outtable(self):
        out = """
            <div class="row-fluid">
            <div class="span2"> 
            <h2 class="title"><a href="%s">%s</a></h2>                     
            <div class="mainphoto grid_3"><a href="%s" class="lightbox">%s</a></div>
             </div>
             </div>
             """
        output = ''
        rowstr = '<div class="row-fluid">'
        colsnum = self.PerRowPrdtNum
        imglists = self.mainimage()
        total = len(imglists['title'])
        span_num = self.span_num()
        rowsnum = (total + colsnum - 1)/colsnum
#        import pdb 
#        pdb.set_trace()
        for i in range(rowsnum):
            output = output + rowstr
            for j in range(colsnum):
                s = i * colsnum + j
#                import pdb
#                pdb.set_trace()
                if s == total:
                    break
                output = output + '<div class="%s"><h2 class="title"><a title="%s" href="%s">%s</a></h2><div class="mainphoto grid_3"><a href="%s" title="%s" class="lightbox">%s</a></div></div>' \
                %(span_num,imglists['title'][s],imglists['imgurl'][s],imglists['title'][s],imglists['large'][s],imglists['caption'][s],imglists['preview'][s])
            output = output + '</div>'
            
        return output

        

    
class storeview(baseview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('storeview') 
        
    @memoize
    def swich_img(self):
        out = """
        jq("li.imgli").bind("mouseenter",function(){
        imgobj = jq(this).find('img');
        tit = imgobj.attr('alt');
        smsrc = imgobj.attr('src');
        bgsrc = smsrc.replace('/tile','/large');
        mdsrc = smsrc.replace('/tile','/mini');        
        newa="<a id='bigphoto' href='"+bgsrc+"' class='jqzoom' title='"+tit+"'><img src='"+mdsrc+"' alt='"+tit+"' /></a>";
        jq("#bigphoto").replaceWith(newa);
        jq(".jqzoom").jqzoom(); 
        })"""
        return out
            
          
class barsview(baseview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('barsview')    

    @memoize
    def barview(self,scale="large",multiline=False):
        "genarator bars html for AJAX load"
        headstr =''
        bodystr = ''
        items = self.imgitems_fast(scale=scale)

        try:
            lenth = len(items['titl'])
            if bool(multiline):
                for i in range(lenth):
                    headstr = headstr + '<link url="%s" /><title text="%s"> </title>' % (items['url'][i],items['titl'][i])
                    bodystr = bodystr + '<div class="banner"><a href="%s"><img src="%s" alt="%s" />%s</a></div>' \
                    % (items['link'][i],items['src'][i],items['titl'][i],items['txt'][i])                
            else:
                for i in range(lenth):
                    headstr = headstr + '<link url="%s" /><title text="%s"> </title>' % (items['url'][i],items['titl'][i])
                    bodystr = bodystr + '<div class="banner"><a href="%s"><img src="%s" alt="%s" /></a></div>' \
                    % (items['link'][i],items['src'][i],items['titl'][i])                
        except:
            pass
        bars = {}
        bars['hstr'] = headstr
        bars['bstr'] = bodystr
        return bars
    
                    
    @memoize
    def imgitems_fast(self,fieldname="image",scale="large",tab=u"，"):
        brains = self.prdt_images()
        items = {}
        items['titl'] = []
        items['url'] = []
        items['link'] = []        
        items['src'] = []
        items['txt'] = []     
        
        if scale == "orig":
            for bn in brains:
                base = bn.getURL()
                try:
                    link2 = bn.linkurl
                except:
                    link2 = ""
                if link2 == "":  link2 = base                
                items['titl'].append(bn.Title)
                dsp = self.splittxt(bn.Description, tab)
                items['txt'].append(dsp)
                items['url'].append(base)
                items['link'].append(link2)  
                items['src'].append(base + "/@@images/" + fieldname)          
            return items
        else:            
            for bn in brains:
                base = bn.getURL()
                try:
                    link2 = bn.linkurl
                except:
                    link2 = ""
                if link2 == "":  link2 = base                
                items['titl'].append(bn.Title)
                dsp = self.splittxt(bn.Description, tab)
                items['txt'].append(dsp)
                items['url'].append(base)
                items['link'].append(link2)                
                items['src'].append(base + "/@@images/" + fieldname + "/" + scale)        
            return items

    def splittxt(self,dsp,tab):
        
        """ """
        if dsp == None:
            return None
        try:
            dsplist = dsp.split(tab)
        except:
            dsplist = dsp.split(",")
        k = len(dsplist)
        sp1 = "<span>"
        sp2 = "</span>"
        dsptxt = "<div class='rollzonetxt'>"
        dsptxtend = "</div>"
        for j in range(k):
            dsptxt = dsptxt + sp1 + dsplist[j] + sp2
            
        dsptxt = dsptxt + dsptxtend
        return dsptxt   


class barsview_mini(barsview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('barsview_mini')  
    
class barsview_thumb(barsview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('barsview_thumb')
    
class barsview_preview(barsview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('barsview_preview')            

class barsview_orig(barsview):
    grok.context(Iproductfolder)
    grok.require('zope2.View')
    grok.name('barsview_orig')    