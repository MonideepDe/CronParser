import pytest
from src.cron_parser import cron_parser
from src.exceptions import InvalidCronFormatException


def test_parse_success():
    # minute - wildcard with division, hour - single number, day_of_month - list, month - wildcard, day of week - range with division (lower bound divisible by divisor)
    parsed_output = cron_parser.parse("*/15 0 1,15 * 2-5/2 /usr/bin/find")
    assert parsed_output == "minute        0 15 30 45\nhour          0\nDAY_OF_MONTH  1 15\nMONTH         1 2 3 4 5 6 7 8 9 10 11 12\nDAY_OF_WEEK   2 4\nCOMMAND       /usr/bin/find"

    # minute - wildcard only
    parsed_output = cron_parser.parse("* 0 1,15 * 2-6/2 /usr/bin/find")
    assert parsed_output == "minute        0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59\nhour          0\nDAY_OF_MONTH  1 15\nMONTH         1 2 3 4 5 6 7 8 9 10 11 12\nDAY_OF_WEEK   2 4 6\nCOMMAND       /usr/bin/find"

    # day of week - range where lower bound not divisible , but upper bound is divisible
    parsed_output = cron_parser.parse("*/15 0 1,15 * 2-6/3 /usr/bin/find")
    assert parsed_output == "minute        0 15 30 45\nhour          0\nDAY_OF_MONTH  1 15\nMONTH         1 2 3 4 5 6 7 8 9 10 11 12\nDAY_OF_WEEK   3 6\nCOMMAND       /usr/bin/find"


def test_parse_bad_input():
    with pytest.raises(InvalidCronFormatException) as e:
        cron_parser.parse("0 1,15 * 2-7/2 /usr/bin/find")

    with pytest.raises(SyntaxError) as e:
        cron_parser.parse("*/15 0 1,15 * 4-2/2 /usr/bin/find")
    assert e.value.msg == "Internal error: DAY_OF_WEEK is not a valid cron field."


def test_parse_bad_inputs():
    with pytest.raises(InvalidCronFormatException) as e:
        cron_parser.parse("0 1,15 * 2-7/2 /usr/bin/find")

    with pytest.raises(SyntaxError) as e:
        cron_parser.parse("*/15 0 1,15 * 4-2/2 /usr/bin/find")
    assert e.value.msg == "Internal error: DAY_OF_WEEK is not a valid cron field."


def test__get_cron_components_success():
    cron_components = cron_parser._get_cron_components(
        "*/15 0 1,15 * 2-5/2 /usr/bin/find")
    assert cron_components["MINUTE"] == ["*/15"]
    assert cron_components["HOUR"] == ["0"]
    assert cron_components["DAY_OF_MONTH"] == ["1", "15"]
    assert cron_components["MONTH"] == ["*"]
    assert cron_components["DAY_OF_WEEK"] == ["2-5/2"]
    assert cron_components["COMMAND"] == ["/usr/bin/find"]


def test__get_cron_components_one_component_missing():
    with pytest.raises(InvalidCronFormatException):
        _ = cron_parser._get_cron_components(
            "*/15 0 1,15 * /usr/bin/find")
