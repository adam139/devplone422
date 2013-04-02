import json
from five import grok

from Acquisition import aq_inner
from zope.interface import Interface

class ModifyDescription(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Interface)
    grok.name('modify-description')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
        data = self.request.form
        description = {'description':context.setDescription(data['description'])}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(description)

class ModifyTitle(grok.View):
    """AJAX action for Modifying title & description.
    """
    
    grok.context(Interface)
    grok.name('modify-title')
    grok.require('zope2.View')
        
    def render(self):
        context = aq_inner(self.context)
        data = self.request.form
        title = {'title':context.setTitle(data['title'])}
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(title)

