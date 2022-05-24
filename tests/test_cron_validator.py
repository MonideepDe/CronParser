from src.cron_validator import cron_validator
from src.constants import MINUTE, HOUR, DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND
from src.exceptions import CronComponentValidationException
import pytest


def test_lowest_range():
    cron_component_dict = {
        MINUTE: "0",
        HOUR: "0",
        DAY_OF_MONTH: "1",
        MONTH: "1",
        DAY_OF_WEEK: "0",
        COMMAND: ""
    }
    cron_validator.validate_cron_components(cron_component_dict)


def test_highest_range():
    cron_component_dict = {
        MINUTE: "59",
        HOUR: "12",
        DAY_OF_MONTH: "31",
        MONTH: "12",
        DAY_OF_WEEK: "6",
        COMMAND: ""
    }
    cron_validator.validate_cron_components(cron_component_dict)


def test_lower_than_allowed_lowest():
    cron_component_dict = {
        MINUTE: "-1",
        HOUR: "-1",
        DAY_OF_MONTH: "0",
        MONTH: "0",
        DAY_OF_WEEK: "-1",
        COMMAND: ""
    }
    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_higher_than_allowed_highest():
    cron_component_dict = {
        MINUTE: "60",
        HOUR: "24",
        DAY_OF_MONTH: "32",
        MONTH: "13",
        DAY_OF_WEEK: "7",
        COMMAND: ""
    }
    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_wildcard():
    cron_component_dict = {
        MINUTE: "*",
        HOUR: "*",
        DAY_OF_MONTH: "*",
        MONTH: "*",
        DAY_OF_WEEK: "*",
        COMMAND: ""
    }

    cron_validator.validate_cron_components(cron_component_dict)


def test_wildcard_with_division():
    cron_component_dict = {
        MINUTE: "*/1",
        HOUR: "*/1",
        DAY_OF_MONTH: "*/1",
        MONTH: "*/1",
        DAY_OF_WEEK: "*/1",
        COMMAND: ""
    }

    cron_validator.validate_cron_components(cron_component_dict)


def test_wildcard_with_division_by_zero():
    cron_component_dict = {
        MINUTE: "*/0",
        HOUR: "*/0",
        DAY_OF_MONTH: "*/0",
        MONTH: "*/0",
        DAY_OF_WEEK: "*/0",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_range():
    cron_component_dict = {
        MINUTE: "0-59",
        HOUR: "0-23",
        DAY_OF_MONTH: "1-31",
        MONTH: "1-12",
        DAY_OF_WEEK: "0-6",
        COMMAND: ""
    }

    cron_validator.validate_cron_components(cron_component_dict)


def test_larger_invalid_range():
    cron_component_dict = {
        MINUTE: "0-60",
        HOUR: "0-24",
        DAY_OF_MONTH: "1-32",
        MONTH: "1-13",
        DAY_OF_WEEK: "0-7",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_lower_invalid_range():
    cron_component_dict = {
        MINUTE: "-1-59",
        HOUR: "-1-23",
        DAY_OF_MONTH: "0-31",
        MONTH: "0-12",
        DAY_OF_WEEK: "-1-6",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_wildcard_with_range():
    cron_component_dict = {
        MINUTE: "*-59",
        HOUR: "*-23",
        DAY_OF_MONTH: "*-31",
        MONTH: "*-12",
        DAY_OF_WEEK: "*-6",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_range_with_division():
    cron_component_dict = {
        MINUTE: "0-59/2",
        HOUR: "0-23/2",
        DAY_OF_MONTH: "1-31/3",
        MONTH: "1-12/3",
        DAY_OF_WEEK: "0-6/2",
        COMMAND: ""
    }

    cron_validator.validate_cron_components(cron_component_dict)


def test_comma():
    cron_component_dict = {
        MINUTE: "0,1,2,59",
        HOUR: "0,1,23",
        DAY_OF_MONTH: "1,2,30,31",
        MONTH: "1,12",
        DAY_OF_WEEK: "0,1,6",
        COMMAND: ""
    }

    cron_validator.validate_cron_components(cron_component_dict)


def test_comma_with_values_lower_than_allowed():
    cron_component_dict = {
        MINUTE: "-1,0,1,2,59",
        HOUR: "-1,0,1,23",
        DAY_OF_MONTH: "0,1,2,30,31",
        MONTH: "0,1,12",
        DAY_OF_WEEK: "-1,0,1,6",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_comma_with_values_higher_than_allowed():
    cron_component_dict = {
        MINUTE: "0,1,2,59,60",
        HOUR: "0,1,23,24",
        DAY_OF_MONTH: "1,2,30,31,32",
        MONTH: "1,12,13",
        DAY_OF_WEEK: "0,1,6,7",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"


def test_comma_with_division():
    cron_component_dict = {
        MINUTE: "0,1,2,59/2",
        HOUR: "0,1,23/3",
        DAY_OF_MONTH: "1,2,30,31/2",
        MONTH: "1,12/2",
        DAY_OF_WEEK: "0,1,6/2",
        COMMAND: ""
    }

    with pytest.raises(CronComponentValidationException) as e:
        cron_validator.validate_cron_components(cron_component_dict)
    assert e.value.message == "Invalid cron components: MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK"
