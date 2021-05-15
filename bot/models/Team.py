from .Channel import Channel
import common.functions as fn


class Team:
    """Defines a Microsoft Teams team.

    Attributes:
        name: name of a Team
        id_: id of a Team
    """

    def __init__(self, name, id_, channels: list[Channel]=None):
        self.name = name
        self.id_ = id_
        self._channels = self.get_channels() or channels

    def __repr__(self):
        channels = "\t".join([str(_) for _ in self.channels])
        msg = f"[TEAM]: {self.name} [CHANNELS]: {channels}\n"
        line = "-" * 15
        return msg + line

    @property
    def channels(self) -> list[Channel]:
        """:obj:`list` of :obj:`Channel`: the channels available for the team"""
        return self._channels

    @channels.setter
    def channels(self, value):
        self._channels = value

    def get_element(self):
        team_header = fn.browser.find_element_by_css_selector(f"h3[id='{self.id_}'")
        team_element = team_header.find_element_by_xpath("..")
        return team_element

    def get_channels(self) -> list[Channel]:
        # Find the channels block and expand it.
        try:
            self.get_element().find_element_by_css_selector("div.channels")
        except fn.exceptions.NoSuchElementException:
            try:
                self.get_element().click()
                self.get_element().find_element_by_css_selector("div.channels")
            except (fn.exceptions.NoSuchElementException,
                    fn.exceptions.ElementNotInteractableException,
                    fn.exceptions.ElementClickInterceptedException):
                return None

        channels_selector = ".channels > ul > ng-include > li"
        channels = self.get_element().find_elements_by_css_selector(channels_selector)

        names = [channel.get_attribute("data-tid") for channel in channels]
        names = [name[name.find("channel-") + 8:name.find("-li")] for name in names if name is not None]
        ids = [channel.get_attribute("id").replace("channel-", "") for channel in channels]
        # Check if the channel has a meeting right now.
        meeting_states_selector = "a > active-calls-counter"
        meeting_states = []
        for channel in channels:
            try:
                channel.find_element_by_css_selector(meeting_states_selector)
                meeting_states.append(True)
            except fn.exceptions.NoSuchElementException:
                meeting_states.append(False)

        return [Channel(names[i], ids[i], has_meeting=meeting_states[i]) for i in range(len(names))]