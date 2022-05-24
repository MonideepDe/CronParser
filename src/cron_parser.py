from src.constants import DAY_OF_MONTH, DAY_OF_WEEK, HOUR, MINUTE, COMMAND, MONTH
from src.exceptions import InvalidCronFormatException


class CronParser:
    def __init__(self) -> None:
        self.cron_components_num = 6
        self.cron_format = [MINUTE, HOUR,
                            DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND]

    def _get_cron_components(self, cron_str: str) -> dict:
        """Gets the 6 components of a cron entry - 
            MINUTE, HOUR,DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND

        Args:
            cron_str (str): Input cron entry string

        Raises:
            InvalidCronFormatException: Exception raised when format of input cron entry is invalid

        Returns:
            dict: Mapping of cron components and its corresponding substring, extracted from input cron entry string
        """
        cron_str_split = cron_str.split(" ")

        if len(cron_str_split) != self.cron_components_num:
            raise InvalidCronFormatException()

        return {self.cron_format[idx]: component_str for idx, component_str in enumerate(cron_str_split)}

    def parse(self, cron_entry: str) -> str:
        cron_component_dict = self._get_cron_components(cron_entry)
        return "parsed"


cron_parser = CronParser()
