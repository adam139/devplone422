from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFCore.utils import getToolByName

from dexterity.membrane.content.member import IMember

from collective.conference import MessageFactory as _

def is_url(value):
    """Is this a URL?

    >>> is_url("http://google.com/")
    True
    >>> is_url("https://google.com")
    True
    >>> is_url("http://example.org/folder/somepage")
    True
    >>> is_url("ssh://google.com")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("nothing")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url("")
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(None)
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link
    >>> is_url(object())
    Traceback (most recent call last):
    ...
    Invalid: Not a valid link

    """
    if isinstance(value, basestring):
        pattern = re.compile(r"^https?://[^\s\r\n]+")
        if pattern.search(value.strip()):
            return True
    raise Invalid(_(u"Not a valid link"))
# Interface class; used to define content-type schema.

class IParticipant(form.Schema, IImageScaleTraversable):
    """
    Conference Participant
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/participant.xml to define the content type
    # and add directives here as necessary.
#    last_name = schema.TextLine(
#        title=_(u"Last Name"),
#        required=True,
#        )
#    
#    first_name = schema.TextLine(
#        title=_(u"First Name"),
#        required=True,
#        )   
    title = schema.TextLine(title=_(u"Full name"),
            required=True)
    email = schema.TextLine(
        title=_(u"Email address"),
        description=_(u"Please input correct mail address,the active code will be sent to it"),        
        required=True,
    ) 

    description = schema.Text(
        title=_(u"Short Bio"),
        description=_(u"Tell us more about yourself"),
        required=False,
    )
    
    homepage = schema.TextLine(
        # url format
        title=_(u"External Homepage"),
        required=False,
        constraint=is_url,
        )   
    
    phone = schema.TextLine(
        title=_(u"Phone number"),
        required=True
    )
    
    form.fieldset('work',
            label=_(u"Work"),
            fields=['organization', 'sector','position', 'research_domain']
    )
    
    organization = schema.TextLine(
        title=_(u"Organization / Company"),
        required=True,
    )
    
    sector = schema.Choice(
        title=_(u"Sector"),
        required=True,
        vocabulary="dexterity.membrane.vocabulary.sector"
        )        

    position = schema.TextLine(
        title=_(u"Position / Role in Organization"),
        required=True,
    )     
        
    research_domain = schema.TextLine(

        title=_(u"research domain"),
        required=False,

        )
           
    form.fieldset('geography',
            label=_(u"Geography"),
            fields=['country', 'province','address']
    )
    
    country = schema.Choice(
        title=_(u"Country"),
        description=_(u"Where you are from"),
        required=False,
        vocabulary="collective.conference.vocabulary.countries"
    )

    province = schema.Choice(
        title=_(u"the province of your company"),
        vocabulary="dexterity.membrane.vocabulary.province",        
        required=True,
        ) 

    address = schema.TextLine(
        title=_(u"personal address"),       
        required=False,
        ) 
            
    bonus = schema.Int(
        # url format
        title=_(u"bonus"),
        required=False,
#        constraint=is_url,
        )    
    
    qq_number = schema.Int(
        # url format
        title=_(u"QQ Number"),
        required=False,

        )          

    form.widget(bio="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    bio = schema.Text(
        title=_(u"Biography"),
        required=False,
        )
    
    photo = NamedBlobImage(
        title=_(u"Photo"),
        description=_(u"Your photo or avatar. Recommended size is 150x195"),
        required=False
    )
      


#    phone = schema.TextLine(
#        title=_(u"Phone number"),
#        required=False
#    )
#
#    organization = schema.TextLine(
#        title=_(u"Organization / Company"),
#        required=False,
#    )
#
#    position = schema.TextLine(
#        title=_(u"Position / Role in Organization"),
#        required=False,
#    )
#
#    country = schema.Choice(
#        title=_(u"Country"),
#        description=_(u"Where you are from"),
#        required=False,
#        vocabulary="collective.conference.vocabulary.countries"
#    )



    is_vegetarian = schema.Bool(
        title=_(u"Vegetarian?"),
        required=False
    )

    tshirt_size = schema.Choice(
        title=_(u"T-shirt size"),
        vocabulary="collective.conference.vocabulary.tshirtsize",
        required=False
    )

    photo = NamedBlobImage(
        title=_(u"Photo"),
        description=_(u"Your photo or avatar. Recommended size is 150x195"),
        required=False
    )

    form.fieldset('sponsorship',
            label=_(u"Funding"),
            fields=['need_sponsorship', 'roomshare', 'comment']
    )

    need_sponsorship = schema.Bool(
            title=_(u"Need funding"),
            description=_(u"Check this option if you need funding to attend."), required=False)

    roomshare = schema.Bool(
            title=_(u"Roomshare"),
            description=_(u"If you want or need a room, check this option"),
            required=False)

    comment = schema.Text(
        title=_(u"Comments"),
        description=_(u"Fill in this field with things you need the organizers to know.\
        If you are roomsharing and already have a roommate, please mention your roommate's name here"),
        required=False
    )

    form.widget(color="collective.z3cform.colorpicker.colorpickeralpha.ColorpickerAlphaFieldWidget")
    color = schema.TextLine(
        title=_(u"Person Color Tag"),
        default=u'cccccc',
        required=False
    )

    
    form.omitted('bonus')   


@form.validator(field=IParticipant['photo'])
def maxPhotoSize(value):
    if value is not None:
        if value.getSize()/1024 > 512:
            raise schema.ValidationError(_(u"Please upload image smaller than 512KB"))



@form.validator(field=IParticipant['email'])
def emailValidator(value):
    try:
        return checkEmailAddress(value)
    except:
        raise Invalid(_(u"Invalid email address"))

class Participant(dexterity.Item):
    grok.implements(IParticipant)
    grok.provides(IParticipant)


    def sessions(self):
        catalog = getToolByName(self, 'portal_catalog')
        result =  catalog({
            'path': {
                'query': '/'.join(self.getConference().getPhysicalPath()),
                'depth': 2
            }, 'portal_type': 'collective.conference.session',
            'emails': self.email
        })
        return [i.getObject() for i in result]
