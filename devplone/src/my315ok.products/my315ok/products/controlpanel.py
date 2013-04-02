from plone.z3cform import layout

from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from my315ok.products.interfaces import IMy315okProductsSettings
from my315ok.products import MessageFactory as _

class My315okProductsControlPanelForm(RegistryEditForm):
    schema = IMy315okProductsSettings
    
    label = _(u"My315okProducts control panel")
    
My315okProductsControlPanelView = layout.wrap_form(My315okProductsControlPanelForm, ControlPanelFormWrapper)
