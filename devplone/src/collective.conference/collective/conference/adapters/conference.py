#-*- coding: UTF-8 -*-
import json

from five import grok
from BTrees.OOBTree import OOSet

from Acquisition import aq_parent

from collective.conference.conference import IConference

from collective.conference.events import LikeEvent,UnlikeEvent,FavoriteEvent,UnFavoriteEvent
from collective.conference.interfaces import IEvaluate,ILikeEvent,IUnlikeEvent,IFavoriteEvent,IUnFavoriteEvent

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



APPROVED_KEY = 'collective.conference.approved'

DISAPPROVED_KEY = 'collective.conference.disapproved'

FAVORITE_KEY = 'collective.conference.favorite'
FOLLOWED_KEY = 'collective.conference.follow'

class evalute(grok.Adapter):
    grok.provides(IEvaluate)
    grok.context(IConference)
    
    def __init__(self, context):
        self.context = context        
        annotations = IAnnotations(context)
        self.approved = annotations.setdefault(APPROVED_KEY, OOSet())
        self.disapproved = annotations.setdefault(DISAPPROVED_KEY, OOSet())
        self.favorite = annotations.setdefault(FAVORITE_KEY, OOSet())
        self.followed = annotations.setdefault(FOLLOWED_KEY, OOSet())        

    #Statistics concern the number of
    @property
    def followerNum(self):
        total = len(self.followed)
        return total
        
    #Determine whether to be concerned about
    def available(self, userToken):
        return self.followed.has_key(userToken) 
    
    #Editing statistics concern the number of               
    def addfollow(self, userToken):
#        import pdb
#        pdb.set_trace()
        if not self.available(userToken):
            self.followed.insert(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)
        
    #Editing statistics concern the number of               
    def delfollow(self, userToken):
        if self.available(userToken):
            self.followed.remove(userToken)
        else:
           raise KeyError("The %s is not concerned about" % userToken)
    
# 赞成票数
    @property
    def voteNum(self):
        VoteNum = len(self.approved)
        return VoteNum
#指定用户是否有权限投赞成票          
    def voteavailableapproved(self,userToken):
        return self.approved.has_key(userToken)
#指定用户是否有权限投反对票          
    
    def voteavailabledisapproved(self,userToken):
        return self.disapproved.has_key(userToken)

#指定用户投赞成票      
    def agree(self, userToken):

        if not self.voteavailableapproved(userToken):
           self.approved.insert(userToken)
        elif  self.voteavailableapproved(userToken):
            self.disapproved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)

#指定用户投反对票   
                  
    def disagree(self,userToken):
        if not self.voteavailabledisapproved(userToken):
            self.disapproved.insert(userToken)
        elif  self.voteavailabledisapproved(userToken):
            self.disapproved.remove(userToken)
        else:
            raise KeyError("Ratings not available for %s" % userToken)

#指定用户是否有权限收藏
        
    def favavailable(self, userToken):

        return  not self.favorite.has_key(userToken)  

#指定用户是执行收藏  
    
    def addfavorite(self,userToken):
        if not self.favavailable(userToken):
            self.favorite.insert(userToken)
        else:
            raise KeyError("The %s is concerned about" % userToken)

#指定用户是取消收藏  
    
    def delfavorite(self,userToken):
        if self.favavailable(userToken):
            self.favorite.remove(userToken)
        else:
           raise KeyError("The %s is not concerned about" % userToken)
        
