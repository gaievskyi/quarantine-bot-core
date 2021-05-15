class ConfigError(Exception):
    """Config was not loaded correctly"""

    def __init__(self,
                 msg="Invalid config data. Check environmental entries"):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


class NoSignInDataError(ConfigError):
    """Raised if any data in config (email or password) is not specified"""

    def __init__(self,
                 msg="Password or email isn't specified. Check environmental entries"):
        self.msg = msg
        super().__init__(self.msg)
