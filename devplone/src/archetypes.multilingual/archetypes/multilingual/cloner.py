# -*- coding: utf-8 -*-
from zope import interface

from plone.multilingual.interfaces import ILanguageIndependentFieldsManager
from plone.multilingual.interfaces import ITranslationCloner


class Cloner(object):

    interface.implements(ITranslationCloner)

    def __init__(self, context):
        self.context = context

    def __call__(self, obj):
        li_clonner = ILanguageIndependentFieldsManager(self.context)
        li_clonner.copy_fields(obj)
