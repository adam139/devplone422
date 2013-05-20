#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent

from dexterity.membrane.interfaces import ICreateMembraneEvent,ICreateBonusRecorderEvent

class CreateMembraneEvent(object):
    interface.implements(ICreateMembraneEvent)
    
    def __init__(self,id,email,password,title,description,homepage,phone,organization,\
                 sector,position,province,address):
        """角色,级别,备注"""
        self.id = id
        self.email = email
        self.password = password
        self.title = title 
        self.description = description
        self.homepage = homepage
        self.phone = phone
        self.organization = organization 
        self.sector = sector
        self.position = position
        self.province = province 
        self.address = address
         
class CreateBonusRecordEvent(object):
    interface.implements(ICreateBonusRecorderEvent)
    
    def __init__(self,who,when,what,obj_title,obj_url,result,bonus):
        """recorder text
        who
        when
        what
        result
        bonus """
        self.who = who
        self.when = when
        self.what = what
        self.obj_title = obj_title
        self.obj_url = obj_url
        self.result = result
        self.bonus = bonus        
                        
       