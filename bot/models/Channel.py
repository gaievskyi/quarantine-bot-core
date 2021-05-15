class Channel:
    """Defines a channel of a team.

    Attributes:
        name (str): name of the channel
        id_ (str): id of the channel
        has_meeting (bool): if the channel has a meeting now.
                            Defaults to False.
    """

    def __init__(self, name, id_, has_meeting=False):
        self.name = name
        self.id_ = id_
        self.has_meeting = has_meeting

    def __repr__(self):
        return f"{self.name}" + (" *MEETING*" if self.has_meeting else "")