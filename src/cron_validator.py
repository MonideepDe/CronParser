from src.exceptions import CronComponentValidationException
import re
from src.constants import MINUTE, HOUR, DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND


class CronValidator:
    def __init__(self) -> None:
        self._minute_regex = re.compile(
            "^(([0-5][0-9]|[0-9])(,([0-5][0-9]|[0-9]))+)|^(\*|([0-5][0-9]|[0-9])((-)([0-5][0-9]|[0-9]))?)(\/([1-5][0-9]|[1-9]))?")
        self._hour_regex = re.compile(
            "^(([0-1][0-9]|2[0-3]|[0-9])(,([0-1][0-9]|2[0-3]|[0-9]))+)|^(\*|(([0-1][0-9]|2[0-3]|[0-9])((-)([0-1][0-9]|2[0-3]|[0-9]))?))(\/([1-1][0-9]|2[0-3]|[1-9]))?")
        self._day_of_month_regex = re.compile(
            "^(([1-2][0-9]|3[0-1]|[1-9])(,([1-2][0-9]|3[0-1]|[1-9]))+)|^(\*|(([1-2][0-9]|3[0-1]|[1-9])((-)([1-2][0-9]|3[0-1]|[1-9]))?))(\/([1-2][0-9]|3[0-1]|[1-9]))?")
        self._month_regex = re.compile(
            "^((1[0-2]|[1-9])(,(1[0-2]|[1-9]))+)|^(\*|((1[0-2]|[1-9])((-)(1[0-2]|[1-9]))?))(\/(1[0-2]|[1-9]))?")
        self._day_of_week_regex = re.compile(
            "^([0-6](,[0-6])+)|^(\*|(([0-6])((-)([0-6]))?))(\/([1-6]))?")
        self._command_regex = re.compile(".*")

        self.component_regex_map = {
            MINUTE: self._minute_regex,
            HOUR: self._hour_regex,
            DAY_OF_MONTH: self._day_of_month_regex,
            MONTH: self._month_regex,
            DAY_OF_WEEK: self._day_of_week_regex,
            COMMAND: self._command_regex
        }

    def validate_cron_components(self, cron_component_dict: dict):
        """
        Validates all cron conponents except the command.
        We expect user to enter valid cron component strings.
        Raises:
            CronComponentValidationException: Exception containing details of invalid components
        """
        all_validity = {cron_component: bool(re.fullmatch(self.component_regex_map[cron_component], cron_component_str))
                        for cron_component, cron_component_str in cron_component_dict.items()}
        if not all(all_validity.values()):
            invalid_components = [cron_component for cron_component,
                                  validity in all_validity.items() if not validity]
            raise CronComponentValidationException(
                f"Invalid cron components: {' '.join(invalid_components)}")


cron_validator = CronValidator()
