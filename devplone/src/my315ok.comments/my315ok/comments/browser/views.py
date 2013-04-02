
import zope.interface
from zope import schema
from zope.component import getUtility

from z3c.form.form import Form
from z3c.form.field import Fields
from z3c.form import button

from plone.app.z3cform import layout
import z3c.form.interfaces
from plone.z3cform import layout
    
try:
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    # z3c.form old version
    from plone.z3cform.textlines import TextLinesFieldWidget

from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

   

from my315ok.comments import cMessageFactory as _
from my315ok.comments.browser.interfaces import IComment

from plone.directives import form
class IComment(form.Schema):
    title = schema.TextLine(title=_(u"Title"))
    author = schema.TextLine(title=_(u"Author"), required=False)
#    form.widget(text=WysiwygFieldWidget)

    text = schema.Text(title=_(u"Text"))   



class CommentAddForm(form.SchemaForm):
    """ z3c.form used to handle the new lead submission.
    
    This form can be rendered  
    
    * standalone (@@comment-form view)
   
    * embedded into the portlet
    
    ..note:: 
        
        It is recommended to use a CSS rule
        to hide form descriptions when rendered in the portlet to save
        some screen estate. 
    
    Example CSS::
    
        .portletComment .formHelp {
           display: none;
        } 
    """
        
    schema = IComment
    
    label = _(u"your comment")
    
    description = _(u"If you are interested in our services leave your comment or suggestion and our sales representatives will contact you.")
    
    ignoreContext = True
    
    def __init__(self, context, request, target_folder=None, returnURLHint=None, full=True):
        """
        
        @param returnURLHint: Should we enforce return URL for this form
        
        @param full: Show all available fields or just required ones.
        """
        form.SchemaForm.__init__(self, context, request)
        self.all_fields = full

        self.container = target_folder
        
        self.returnURLHint = returnURLHint
            
    @property
    def action(self):
        """ Rewrite HTTP POST action.
        
        If the form is rendered embedded on the others pages we 
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.portal_url() + "/@@comment-form"
      
#    def updateWidgets(self):
#        """ Make sure that return URL is not visible to the user.
#        """
#        form.SchemaForm.updateWidgets(self)
#        
#        
#        # Use the return URL suggested by the creator of this form
#        # (if not acting standalone)
#        self.widgets["returnURL"].mode = z3c.form.interfaces.HIDDEN_MODE
#        if self.returnURLHint:
#            self.widgets["returnURL"].value = self.returnURLHint


  
            
    
    
    def postData(self, data):
        """ Post data to comment """             
#        import pdb
#        pdb.set_trace()
        id = data.get("title","")
        
        text = data.get("text","")
        container = self.container
        if id == None:
            return
        obj = getattr(container,id,None)
        if obj == None:           
            container.invokeFactory(type_name="Document", id=id)
            obj = container[id]
        obj.setText(text)
        obj.setTitle(id)


    
    @button.buttonAndHandler(_(u'Post comment'))
    def handleApply(self, action):
        """ Form button hander. """
        
        # data is dict form field name -> cleaned value look-up
        # errors is a list of z3c error objects which have attribute message
        # extractData() also sets self.errors by default
        
        data, errors = self.extractData()
               
        if len(errors) == 0:
        
            self.postData(data)
                
            ok_message = _(u"Thank you for your comments. Our customer services will come back to you in few days")
        
            # Check whether this form was submitted from another page
            returnURL = data.get("returnURL", "")

            if returnURL != "" and returnURL is not None:
                
                # Go to page where we were sent and
                # pass the confirmation message as status message (in session)
                # as we are not in the control of the destination page
                from Products.statusmessages.interfaces import IStatusMessage
                messages = IStatusMessage(self.request)
                messages.addStatusMessage(ok_message, type="info")
                self.request.response.redirect(returnURL)
            else:
                # Act standalone
                self.status = ok_message
        else:
            # errors on the form
            self.status = _(u"Please correct the errors below") 
    

CommentFormView = layout.wrap_form(CommentAddForm)
