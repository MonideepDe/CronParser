class InvalidCronFormatException(Exception):
    pass


class CronComponentValidationException(Exception):
    def __init__(self, message) -> None:
        self.message = message


class InvalidUsageOfSpecialOperators(Exception):
    def __init__(self, message) -> None:
        self.message = message
