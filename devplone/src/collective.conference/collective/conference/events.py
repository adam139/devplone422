#-*- coding: UTF-8 -*-
from zope import interface
from zope.component.interfaces import ObjectEvent

from collective.conference.interfaces import IFollowedEvent
from collective.conference.interfaces import IUnfollowedEvent

from collective.conference.interfaces import IRegisteredConfEvent,IUnRegisteredConfEvent,IRegisteredSessionEvent

from collective.conference.interfaces import ILikeEvent
from collective.conference.interfaces import IUnlikeEvent
from collective.conference.interfaces import IFavoriteEvent
from collective.conference.interfaces import IUnFavoriteEvent
from collective.conference.interfaces import IClickEvent
from collective.conference.interfaces import ICountStatistics
from collective.conference.interfaces import ICreatedMentionmeFolderEvent
from collective.conference.interfaces import ICountNumEvent


    
class FollowedEvent(ObjectEvent):
    interface.implements(IFollowedEvent)



class UnfollowedEvent(ObjectEvent):
    interface.implements(IUnfollowedEvent)
    

    
class LikeEvent(ObjectEvent):
    interface.implements(ILikeEvent)
    
class UnlikeEvent(ObjectEvent):
    interface.implements(IUnlikeEvent)
    
class FavoriteEvent(ObjectEvent):
    """取消收藏事件"""
    interface.implements(IFavoriteEvent)

class UnFavoriteEvent(ObjectEvent):
    interface.implements(IUnFavoriteEvent)   

class CreatedMentionmeFolderEvent(ObjectEvent):
    interface.implements(ICreatedMentionmeFolderEvent)   

class ClickEvent(ObjectEvent):
    interface.implements(IClickEvent)

class CountStatistics(ObjectEvent):
    interface.implements(ICountStatistics)

class CountNumEvent(ObjectEvent):
    interface.implements(ICountNumEvent)  

 

from collective.conference.conference import IConference
from collective.conference.interfaces import IClickEvent


class ClickEvent(ObjectEvent):
    interface.implements(IClickEvent)


class RegisteredConfEvent(ObjectEvent):
    interface.implements(IRegisteredConfEvent)
    
class UnRegisteredConfEvent(ObjectEvent):
    interface.implements(IUnRegisteredConfEvent)    
    
class RegisteredSessionEvent(ObjectEvent):
    interface.implements(IRegisteredSessionEvent)    
