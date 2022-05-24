
import logging

from src.constants import (COMMA, COMMAND, DAY_OF_MONTH, DAY_OF_WEEK, DIVISION,
                           HOUR, MINUTE, MONTH, NO_PROCESSING, RANGE, WILDCARD)
from src.cron_validator import cron_validator
from src.exceptions import (InvalidCronFormatException,
                            InvalidUsageOfSpecialOperators)


class CronParser:
    def __init__(self) -> None:
        self.cron_components_num = 6
        self.cron_format = [MINUTE, HOUR,
                            DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND]
        self._field_range = {
            # FIELD_NAME: [MIN_VALUE, MAX_VALUE]
            MINUTE: [0, 59],
            HOUR: [0, 23],
            DAY_OF_MONTH: [1, 31],
            MONTH: [1, 12],
            DAY_OF_WEEK: [0, 6]
        }
        self._handlers = {WILDCARD: self._handle_wildcard, COMMA: self._handle_comma,
                          RANGE: self._handle_range, DIVISION: self._handle_division, NO_PROCESSING: self._handle_no_processing}
        self._interpretation_order = [
            NO_PROCESSING, COMMA, WILDCARD, RANGE, DIVISION]
        self._interpretation_excluded_components = [COMMAND]

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
        cron_validator.validate_cron_components(cron_component_dict)
        interpreted = self._interpret(cron_component_dict)
        return "parsed"

    def _interpret(self, cron_component_dict: dict):
        """Interprets each component of cron string"""
        cron_component_interpret_dict = {k: v for k, v in cron_component_dict.items(
        ) if k not in self._interpretation_excluded_components}
        classification = self._classify_cron_components(
            cron_component_interpret_dict)

        interpretation = {
            cron_component: self._handlers[cron_component_kind](
                cron_component_str=cron_component_interpret_dict[cron_component],
                cron_component=cron_component,
                classification=classification
            )
            for cron_component_kind in self._interpretation_order for cron_component in classification[cron_component_kind]
        }

        interpretation[COMMAND] = cron_component_dict[COMMAND]
        return interpretation

    def _classify_cron_components(self, cron_component_dict: dict):
        classfication = {WILDCARD: [],
                         COMMA: [], RANGE: [], DIVISION: [], NO_PROCESSING: []}
        for component, component_str in cron_component_dict.items():
            if "*" in component_str:
                classfication[WILDCARD].append(component)
            if "," in component_str:
                classfication[COMMA].append(component)
            if "-" in component_str:
                classfication[RANGE].append(component)
            if "/" in component_str:
                classfication[DIVISION].append(component)

        no_processing_keys = set(cron_component_dict.keys(
        )) - set([cron_comp for cron_comp_list in list(classfication.values()) for cron_comp in cron_comp_list])
        if len(no_processing_keys):
            classfication[NO_PROCESSING].extend(no_processing_keys)
        return classfication

    def _handle_no_processing(self, cron_component_str: str, **argv: dict):
        return cron_component_str

    def _handle_comma(self, cron_component_str: str, **argv: dict):
        logging.info(f"handling comma: {cron_component_str}")
        return [i for i in sorted([int(c) for c in cron_component_str.split(",")])]

    def _handle_wildcard(self, cron_component_str: str, cron_component: str, classification: dict):
        logging.info(f"handling wildcard: {cron_component_str}")
        if cron_component in classification[DIVISION]:
            logging.info("Ignoring ... will be handled by DIVISION handler")
        return [i for i in range(self._field_range[cron_component][0], self._field_range[cron_component][1] + 1)]

    def _handle_range(self, cron_component_str: str, cron_component: str, classification: dict):
        logging.info(f"handling range: {cron_component_str}")
        if cron_component in classification[DIVISION]:
            logging.info("Ignoring ... will be handled by DIVISION handler")
        low, high = cron_component_str.split("/")[0].split("-")
        return [i for i in range(int(low), int(high)+1)]

    def _handle_division(self, cron_component_str: str, cron_component: str, classification: dict):
        logging.info(f"handling division: {cron_component_str}")
        if cron_component in classification[WILDCARD]:
            return self._handle_division_with_wildcard(cron_component_str, cron_component)
        elif cron_component in classification[RANGE]:
            return self._handle_division_with_range(cron_component_str=cron_component_str, cron_component=cron_component)
        else:
            raise InvalidUsageOfSpecialOperators(
                f"Cron Component: {cron_component}. Division operator appears without range or wildcard operator.")

    def _handle_division_with_wildcard(self, cron_component_str, cron_component):
        if cron_component_str.index("*") > cron_component_str.index("/"):
            raise InvalidUsageOfSpecialOperators(
                f"Cron Component: {cron_component}. Range operator (*) should appear before division operator (/)")
        low, high = self._field_range[cron_component]
        div_int = int(cron_component_str.split("/")[-1])
        return [div_int*i for i in range(low, (high//div_int)+1)]

    def _handle_division_with_range(self, cron_component_str, cron_component):
        if cron_component_str.index("-") > cron_component_str.index("/"):
            raise InvalidUsageOfSpecialOperators(
                f"Cron Component: {cron_component}. Range operator (-) should appear before division operator (/)")
        low, high = cron_component_str.split("/")[0].split("-")
        low, high = int(low), int(high)
        if low > high:
            raise SyntaxError(
                f"Internal error: {cron_component} is not a valid cron field.")
        div_int = int(cron_component_str.split("/")[-1])

        low = low if low % div_int == 0 else low + (div_int - low % div_int)
        return [i for i in range(low, high+1, div_int)]


cron_parser = CronParser()
