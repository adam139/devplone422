#-*- coding: UTF-8 -*-
import json

from five import grok
from BTrees.OOBTree import OOSet

from Acquisition import aq_parent

from collective.conference.conference import IConference

from collective.conference.events import FollowedEvent,UnfollowedEvent,LikeEvent,UnlikeEvent,FavoriteEvent,UnFavoriteEvent
from collective.conference.interfaces import IEvaluate,ILikeEvent,IUnlikeEvent,IFavoriteEvent,IUnFavoriteEvent,IFollowedEvent,\
IUnfollowedEvent,IRegisteredConfEvent,IUnRegisteredConfEvent,IRegisteredSessionEvent

from zExceptions import Forbidden
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent
from zope.annotation.interfaces import IAnnotations
from dexterity.membrane.content.member import IMember

from plone.dexterity.utils import createContentInContainer
from Products.CMFCore.utils import getToolByName

from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.app.intid import IntIds
from zope.intid.interfaces import IIntIds
from zope import component

from datetime import datetime

        
@grok.subscribe(IConference, ILikeEvent)
def approve(obj, event):
    """approve the answer"""

    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    agreelist = list(userobject.getProperty('mylike'))
    
    if not obj.id in agreelist:
        agreelist.append(obj.id)
        userobject.setProperties(mylike=agreelist)

    evlute = IEvaluate(obj)
    if not evlute.voteavailableapproved(username):
        evlute.agree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject()
        
@grok.subscribe(IConference, IUnlikeEvent)
def disapprove(obj, event):
    """approve the answer"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject= mp.getAuthenticatedMember()
    username = userobject.getId()
    disagreelist = list(userobject.getProperty('myunlike'))
    
    if not obj.id in disagreelist:
        disagreelist.append(obj.id)
        userobject.setProperties(myunlike=disagreelist)
    
    evlute = IEvaluate(obj)
    if not evlute.voteavailabledisapproved(username):
        evlute.disagree(username)
        obj.voteNum = evlute.voteNum
        obj.totalNum = evlute.voteNum - len(evlute.disapproved)
        obj.reindexObject() 
        
@grok.subscribe(IConference, IFavoriteEvent)
def FavoriteAnswer(obj,event):
    """add the answer to favorite"""
    
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    favoritelist = list(userobject.getProperty('myfavorite'))
    
    if not obj.id in favoritelist:
        favoritelist.append(obj.id)
        userobject.setProperties(myfavorite=favoritelist)
        
    evlute = IEvaluate(obj)
    if not evlute.favavailable(username):
        evlute.addfavorite(username)

@grok.subscribe(IConference, IUnFavoriteEvent)
def UnFavoriteAnswer(obj,event):
    """del the answer from the favorite"""
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    favoritelist = list(userobject.getProperty('myfavorite'))
    
    if  obj.id in favoritelist:
        favoritelist.remove(obj.id)
        userobject.setProperties(myfavorite=favoritelist)
        
    evlute = IEvaluate(obj)
    if evlute.favavailable(username):
        evlute.delfavorite(username)
        
@grok.subscribe(IConference, IObjectRemovedEvent)
def delObjfav(obj,event):
    favoriteevlute = IEvaluate(obj)
    """判断当前答案是否被收藏"""
    answerlist = favoriteevlute.favorite
    if len(answerlist) == 0:
        return
    
    pm = getToolByName(obj, 'portal_membership')
    for answer in answerlist:
        userobject=pm.getMemberById(answer)
        """删除用户收藏到答案"""
        favoritelist = list(userobject.getProperty('myfavorite'))
        favoritelist.remove(obj.getId())

@grok.subscribe(IConference,IFollowedEvent)
def Followed(obj,event):
#    import pdb
#    pdb.set_trace()
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    questionlist = list(userobject.getProperty('myquestions'))
    if not obj.id in questionlist:
        questionlist.append(obj.id)
        userobject.setProperties(myquestions=questionlist)
    evlute = IEvaluate(obj)
    if not evlute.available(username):
        evlute.addfollow(username)
        obj.followernum = evlute.followerNum
        obj.reindexObject()         
    
@grok.subscribe(IConference,IUnfollowedEvent)
def UnFollowed(obj,event):
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getId()
    questionlist = list(userobject.getProperty('myquestions'))
    if obj.id in questionlist:
        questionlist.remove(obj.id)
        userobject.setProperties(myquestions=questionlist)

    evlute = IEvaluate(obj)
    
    if evlute.available(username):
        evlute.delfollow(username)
        obj.followernum = evlute.followerNum
        obj.reindexObject()  

def getMember(context,email):
    catalog = getToolByName(context, "portal_catalog")
    memberbrains = catalog(object_provides=IMember.__identifier__,
                               email=email)

    if len(memberbrains) == 0:return None
    return memberbrains[0].getObject()
    
        
@grok.subscribe(IConference,IRegisteredConfEvent)
def Registered(obj,event):
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
#    username = userobject.getId()
    username = userobject.getUserName()
#    username = "12@qq.com"    
    questionlist = list(userobject.getProperty('conferences'))
    if not obj.id in questionlist:
        questionlist.append(obj.id)
        userobject.setProperties(conferences=questionlist)
    try:
        plists = list(obj.participants)
    except:
        plists = []
 
    if  not username in plists:
        plists.append(username)
        obj.participants= plists
        obj.reindexObject()
                 
    recorders = list(userobject.getProperty('bonusrecorder'))
    member = getMember(obj,username)
    if not(member  is None):
        username = member.title
        member.bonus = member.bonus + 2
        member.reindexObject()
        
    start = datetime.today().strftime('%Y-%m-%d')
    recorder = "%s 于%s因参加活动<a href='%s'>%s</a>而获取%s积分。" %(username,start,obj.absolute_url(),obj.title,2)
    
    recorders.append(recorder)
    userobject.setProperties(bonusrecorder=recorders)
        
@grok.subscribe(IConference,IUnRegisteredConfEvent)
def UnRegistered(obj,event):
    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
    username = userobject.getUserName()

    questionlist = list(userobject.getProperty('conferences'))
    if  obj.id in questionlist:
        questionlist.remove(obj.id)
        userobject.setProperties(conferences=questionlist)
    try:
        plists = list(obj.participants)
    except:
        plists = []
 
    if   username in plists:
        plists.remove(username)
        obj.participants= plists
        obj.reindexObject() 
    recorders = list(userobject.getProperty('bonusrecorder'))
    member = getMember(obj,username)
    if not(member  is None):
        username = member.title
        member.bonus = member.bonus - 2
        member.reindexObject()    
    start = datetime.today().strftime('%Y-%m-%d')
    recorder = "%s 于%s因没有参加活动<a href='%s'>%s</a>而扣除%s积分。" %(username,start,obj.absolute_url(),obj.title,2)
    
    recorders.append(recorder)
    userobject.setProperties(bonusrecorder=recorders)
            
@grok.subscribe(IConference,IRegisteredSessionEvent)
def RegisteredSession(obj,event):

    mp = getToolByName(obj,'portal_membership')
    userobject = mp.getAuthenticatedMember()
#    username = userobject.getId()
    username = userobject.getUserName()
#    username = "12@qq.com"    
    slist = list(userobject.getProperty('speeches'))
    if not obj.id in slist:
        slist.append(obj.id)
        userobject.setProperties(speeches=slist)
#    plists = obj.speakers
    try:
        slists = list(obj.speakers)
    except:
        slists = [] 
    try:
        plists = list(obj.participants)
    except:
        plists = []         
    if  not username in plists:
        plists.append(username)
        obj.participants= plists
    if  not username in slists:              
        slists.append(username)        
        obj.speakers= slists
    obj.reindexObject()             
        