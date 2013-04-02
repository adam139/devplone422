#-*- coding: UTF-8 -*-
import json

from five import grok
from BTrees.OOBTree import OOSet

from Acquisition import aq_parent

from collective.conference.conference import IConference

from collective.conference.events import FollowedEvent,UnfollowedEvent,LikeEvent,UnlikeEvent,FavoriteEvent,UnFavoriteEvent
from collective.conference.interfaces import IEvaluate,ILikeEvent,IUnlikeEvent,IFavoriteEvent,IUnFavoriteEvent,IFollowedEvent,\
IUnfollowedEvent

from zExceptions import Forbidden
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.lifecycleevent.interfaces import IObjectAddedEvent,IObjectRemovedEvent
from zope.annotation.interfaces import IAnnotations


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
        