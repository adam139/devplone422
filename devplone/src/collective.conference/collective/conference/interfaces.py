#-*- coding: UTF-8 -*-
from zope.interface import Interface
from zope import schema
from zope.component.interfaces import IObjectEvent

from collective.conference import MessageFactory as _


class IFollowedEvent(IObjectEvent):
    """pass"""
      
class IUnfollowedEvent(IObjectEvent):
    """ pass"""

class IRegisteredConfEvent(IObjectEvent):
    """ pass"""    

class IUnRegisteredConfEvent(IObjectEvent):
    """ pass"""      

class IRegisteredSessionEvent(IObjectEvent):
    """ pass"""    
        
class ILikeEvent(IObjectEvent):
    """ pass"""

class IUnlikeEvent(IObjectEvent):
    """ pass"""
    
class IFavoriteEvent(IObjectEvent):
    """pass"""
    
class IUnFavoriteEvent(IObjectEvent):
    """pass"""
class ICreatedMentionmeFolderEvent(IObjectEvent):
    """pass"""
class ICountAware(Interface):
    """ the marke interface of that object  can be countted """
    
class ICountNumEvent(IObjectEvent):
    """pass"""
class IClickEvent(IObjectEvent):
    """ Event gets fired when the object was viewed """

class ICountStatistics(IObjectEvent):
    """pass"""
    def updateCount(self):
        """update the count of the site"""
        
    def getCount(self):
        """get the conunt of the site"""
    
    def setCount(self):
        """set the conunt of the site"""

# Adapter question Evaluate
class IEvaluate(Interface):
    followerNum = schema.Int(
            title=_(u"A score from 1-100"),
            readonly=True,
            )
    def available(userToken):
        """Evaluation of the legality of testing(existing users)
        """
                       
    def addquestion(userToken):
        """Give a positive (True) or negative (False) vote.
        """
        
    def delquestion(userToken):
        """Give a positive (True) or negative (False) vote.
        """  

# Adapter answer Evaluate
class IAnswerEvaluate(Interface):

    def voteavailabledisapproved(userToken):
        """  Evaluation of the legality of testing(existing users) 
         """
    def voteavailabledisapproved(userToken):
        """  Evaluation of the legality of testing(existing users) 
         """
    def favavailable(userToken):
        """Evaluation of the legality of testing(existing users)  
         """
    def voteNum(self):
        """the num of people who vote it"""
    
    def agree(userToken):
        """  agree the answer"""
    
    def disagree(userToken):
        """disagree the answer"""
        
    def addfavorite(userToken): 
        """add favoriter """
        
    def delfavorite(userToken): 
        """del favorite"""   
class IClickEvent(IObjectEvent):
    """ Event gets fired when the object was clicked"""