#-*- coding: UTF-8 -*-
from zope import interface
from zope.component import adapts
from zope.component.interfaces import ObjectEvent

from dexterity.membrane.interfaces import ICreateMembraneEvent

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