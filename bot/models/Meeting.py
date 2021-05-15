class Meeting:
    """Defines a Microsoft Teams meeting.

    Attributes:
        id_: id of the meeting
        title: title of the meeting
        time_started: time when meeting started
        channel: channel of the meeting
    """

    def __init__(self, id_, title, channel=None):
        self.id_ = id_
        self.title = title
        self.channel = channel

    def __repr__(self):
        return f"{self.title}"