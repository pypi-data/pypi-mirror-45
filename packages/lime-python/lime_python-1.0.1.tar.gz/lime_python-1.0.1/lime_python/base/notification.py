from lime_python.base.envelope import Envelope
from lime_python.utils.reason import Reason as NotificationReason
from lime_python.utils.reason import ReasonCode
from enum import Enum


class NotificationEvent(Enum):
    """
    Enum of the available notification's events

    Value:
        Failed (str)
        Accepted (str)
        Validated (str)
        Authorized (str)
        Dispatched (str)
        Received (str)
        Consumed (str)
    """

    Failed = 'failed'
    Accepted = 'accepted'
    Validated = 'validated'
    Authorized = 'authorized'
    Dispatched = 'dispatched'
    Received = 'received'
    Consumed = 'consumed'


class Notification(Envelope):
    """
    Representation of a LIME Notification

    Parameters:
        id (str)
        fromN (Node)
        to (Node)
        event (NotificationEvent)
        reason (Reason)
    """

    def __init__(self, id=None, to=None, fromN=None, event=None, reason=None):
        super().__init__(id, fromN, to)

        self.Event = event
        self.Reason = reason

    @property
    def Event(self):
        return self.__Event

    @Event.setter
    def Event(self, event):
        if isinstance(event, str):
            event = NotificationEvent(event)
        if event is not None and not isinstance(event, NotificationEvent):
            raise ValueError('"Event" must be a NotificationEvent')
        self.__Event = event

    @property
    def Reason(self):
        return self.__Reason

    @Reason.setter
    def Reason(self, reason):
        if reason is not None and not isinstance(reason, NotificationReason):
            raise ValueError('"Reason" must be a Reason')
        self.__Reason = reason

    def GetReasonJson(self):
        if self.Reason is not None:
            return self.Reason.ToJson()
        return None

    def ToJson(self):
        json = {
            **super().ToJson(),
            'event': self.Event.value
        }

        if self.Reason is not None:
            json.update({'reason': self.GetReasonJson()})
        return json

    @staticmethod
    def FromJson(inJson):
        if isinstance(inJson, str):
            inJson = json.loads(inJson)
        try:
            reason = (
                'reason' in inJson and
                NotificationReason.FromJson(inJson['reason'])
            ) or None

            envelope = Envelope.FromJson(inJson)

            return Notification(
                envelope.Id,
                envelope.To,
                envelope.From,
                inJson['event'],
                reason
            )
        except KeyError:
            raise ValueError('The given json is not a Notification')
