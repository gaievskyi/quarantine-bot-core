from common.settings import browser
from common.settings import config
from common.constants import greeting

from models.Bot import Bot


def run():
    # Greet us
    print(greeting)
    # Create an instance of the bot
    bot = Bot(config["EMAIL"], config["PASSWORD"])
    # Get to the MS Teams page
    browser.get("https://teams.microsoft.com")
    # bot.do_everything_instead_of_me()
    bot.start()

if __name__ == '__main__':
    run()
