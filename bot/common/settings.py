from . import exceptions

from dotenv import find_dotenv
from dotenv import dotenv_values
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Environment entries
config = dotenv_values(find_dotenv())
if not config:
    raise exceptions.NoSignInDataError

# Settings of the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--no-sandbox")
options.add_argument("--mute-audio")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1,
    "profile":
    {
        "password_manager_enabled": False
    }
})
# Define the browser
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
