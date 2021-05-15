from time import sleep

from selenium.webdriver.common.keys import Keys

from .Team import Team
from .Meeting import Meeting
from ..common.settings import config
from ..common import functions as fn

class User:
    """Defines an Microsoft Teams user.

    Attributes:
        email (str): stores email of the user
        password (str): stores password of the user
    """

    def __init__(self, email: str, password: str, teams: list[Team]=None):
        self.email = email
        self.password = password
        self._teams = teams

    def __repr__(self):
        return (
            f"{self.email}\n"
            f"{self.password}\n"
            f"{self.teams}"
        )

    @property
    def teams(self) -> list[Team]:
        """:obj:`list` of :obj:`Team`: the teams the user is on"""
        return self._teams

    @teams.setter
    def teams(self, value):
        self._teams = value

    @staticmethod
    def get_teams() -> list[Team]:
        selector = "ul>li[role='treeitem']>div[sv-element]"
        teams = fn.browser.find_elements_by_css_selector(selector)

        names = [team.get_attribute("data-tid") for team in teams]
        names = [name[name.find('team-') + 5:name.rfind("-li")] for name in names]

        headers = [team.find_element_by_css_selector("h3") for team in teams]
        ids = [header.get_attribute("id") for header in headers]

        return [Team(names[i], ids[i]) for i in range(len(teams))]


class Bot(User):
    """Simulates behaviour of an Microsoft Teams user.

    Attributes:
        email (str): stores email of the user
        password (str): stores password of the user
    """

    def __init__(self, email, password):
        super().__init__(email, password)

    def start(self):
        self.sign_in()
        sleep(15)
        self.teams = self.get_teams()
        if meetings := self.get_meetings(self.teams):
            for team in self.teams:
                if team.name == config["TEAM"]:
                    for channel in team.channels:
                        if channel.has_meeting:
                            print("> Captain, looks like I've found our lecture!")
                            self.connect(meetings[0])
        else:
            print("> I didn't find any meeting.")

    def sign_in(self) -> None:
        """Sign in to the Microsoft Teams"""

        # Find a login form
        email_class = fn.query_selector("input[type='email']", 30)
        if email_class:
            email_class.send_keys(self.email)
        # Avoid StaleElementReferenceException
        email_class = fn.query_selector("input[type='email']", 5)
        if email_class:
            email_class.send_keys(Keys.ENTER)

        login_class = fn.query_selector("input[type='password']", 10)
        if login_class:
            login_class.send_keys(self.password)
        # Avoid StaleElementReferenceException
        login_class = fn.query_selector("input[type='password']", 5)
        if login_class:
            login_class.send_keys(Keys.ENTER)

        # Accept all proposals to keep logged in and use
        # browser instead of app to log in MS Teams finally.
        keep_logged_in = fn.query_selector("input[id='idBtn_Back']", 5)
        if keep_logged_in:
            keep_logged_in.click()

        use_web_instead = fn.query_selector(".use-app-lnk", 5)
        if use_web_instead:
            use_web_instead.click()

    @staticmethod
    def go_to_calendar():
        calendar_selector = "button.app-bar-link > ng-include > svg.icons-calendar"
        calendar = fn.query_selector(calendar_selector, 5)
        calendar.click() if calendar else None

    @staticmethod
    def go_to_teams():
        teams_selector = "button.app-bar-link > ng-include > svg.icons-teams"
        teams = fn.query_selector(teams_selector, 5)
        teams.click() if teams else None

    def get_meetings(self, teams=None):
        if teams is None:
            teams = self.teams
        meetings = []
        conversations = "https://teams.microsoft.com/_#/conversations/a"
        for team in teams:
            for channel in team.channels:
                if channel.has_meeting:
                    script = f'window.location = "{conversations}a?threadId={channel.id_}&ctx=channel";'
                    fn.browser.execute_script(script)

                    self.go_to_teams()

                    meeting_element = fn.query_selector(".ts-calling-thread-header", 10)
                    if meeting_element is None:
                        continue
                    meeting_elements = fn.browser.find_elements_by_css_selector(".ts-calling-thread-header")
                    for meeting_element in meeting_elements:
                        meeting_id = meeting_element.get_attribute("id")

                        meetings.append(Meeting(id_=meeting_id,
                                                title=f"{team.name} -> {channel.name}",
                                                channel=channel.id_))
        return meetings

    def connect(self, meeting):
        conversations = "https://teams.microsoft.com/_#/conversations/a"

        script = f'window.location = "{conversations}a?threadId={meeting.channel}&ctx=channel";'
        fn.browser.execute_script(script)

        self.go_to_teams()

        btn_selector = f"div[id='{meeting.id_}'] > calling-join-button > button"
        join_btn = fn.query_selector(btn_selector, 5)

        if join_btn is None:
            return None

        fn.browser.execute_script("arguments[0].click()", join_btn)

        join_now_btn = fn.query_selector("button[data-tid='prejoin-join-button']", 30)
        if join_now_btn is None:
            return None

        # Turn off the camera
        selector = "toggle-button[data-tid='toggle-video']>div>button"
        video_btn = fn.browser.find_element_by_css_selector(selector)
        video_is_on = video_btn.get_attribute("aria-pressed")
        if video_is_on == "true":  # "true" must be a string
            video_btn.click()
            print("> Turned off the Video.")

        # Turn off the microphone
        selector = "toggle-button[data-tid='toggle-mute']>div>button"
        audio_btn = fn.browser.find_element_by_css_selector(selector)
        audio_is_on = audio_btn.get_attribute("aria-pressed")
        if audio_is_on == "true":  # Not a mistake!
            audio_btn.click()
            print("> Turned off the Audio.")

        # Avoid StaleElementReferenceException
        selector = "button[data-tid='prejoin-join-button']"
        join_now_btn = fn.query_selector(selector, 5)
        if join_now_btn is None:
            return None
        join_now_btn.click()

        print(f"> Just have joined the meeting on {meeting}")