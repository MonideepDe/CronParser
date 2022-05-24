import pytest
from src.cron_parser import cron_parser
from src.exceptions import InvalidCronFormatException


def test_parse_success():
    parsed_output = cron_parser.parse("*/15 0 1,15 * 2-5/2 /usr/bin/find")
    assert parsed_output == "parsed"


def test__get_cron_components_success():
    cron_components = cron_parser._get_cron_components(
        "*/15 0 1,15 * 2-5/2 /usr/bin/find")
    assert cron_components["MINUTE"] == "*/15"
    assert cron_components["HOUR"] == "0"
    assert cron_components["DAY_OF_MONTH"] == "1,15"
    assert cron_components["MONTH"] == "*"
    assert cron_components["DAY_OF_WEEK"] == "2-5/2"
    assert cron_components["COMMAND"] == "/usr/bin/find"


def test__get_cron_components_one_component_missing():
    with pytest.raises(InvalidCronFormatException):
        _ = cron_parser._get_cron_components(
            "*/15 0 1,15 * /usr/bin/find")
