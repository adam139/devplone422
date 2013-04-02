from plone.indexer.decorator import indexer
from Products.ZCatalog.interfaces import IZCatalog
from five import grok
from collective.conference.conference import IConference
from collective.conference.session import ISession
from collective.conference.participant import IParticipant
from collective.conference.interfaces import IEvaluate


@indexer(IConference)
def c_conference_rooms(obj, **kw):
    return obj.rooms

@indexer(IConference)
def c_conference_province(obj, **kw):
    return obj.province

@indexer(IConference)
def c_conference_sponsor(obj, **kw):
    return obj.sponsor

@indexer(IConference)
def c_conference_type(obj, **kw):
    return obj.conference_type

@indexer(IConference)
def c_conference_startDate(obj, **kw):
    return obj.startDate

@indexer(ISession)
def s_conference_rooms(obj, **kw):
    return obj.conference_rooms

@indexer(IParticipant)
def p_emails(obj, **kw):
    return [obj.email]


@indexer(IConference,IZCatalog)
def followernum(context):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``name`` index with the topic .
    """
    return IEvaluate(context).followerNum

@indexer(IConference)
def conferenceClickNum(obj,**kw):
    """Create a catalogue indexer, registered as an adapter, which can
    populate the ``totalNum`` index with the conference .    """
    
    return obj.clicknum
