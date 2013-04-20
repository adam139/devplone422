from zope.interface import Interface

from membrane.usersinout import UsersInOutMessageFactory as _

class IUsersInOutLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """
