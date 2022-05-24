from src.cron_parser import cron_parser
from src.constants import MINUTE, HOUR, DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND


def test__interpretor_lowest_range():
    cron_component_dict = {
        MINUTE: "0",
        HOUR: "0",
        DAY_OF_MONTH: "1",
        MONTH: "1",
        DAY_OF_WEEK: "0",
        COMMAND: ""
    }
    interpreted = cron_parser._interpret(cron_component_dict)
    expected_interpretation = {'MINUTE': '0', 'DAY_OF_WEEK': '0',
                               'DAY_OF_MONTH': '1', 'HOUR': '0', 'MONTH': '1', 'COMMAND': ''}
    assert interpreted == expected_interpretation


def test__interpretor_wildcard():
    cron_component_dict = {
        MINUTE: "*",
        HOUR: "*",
        DAY_OF_MONTH: "*",
        MONTH: "*",
        DAY_OF_WEEK: "*",
        COMMAND: ""
    }
    interpreted = cron_parser._interpret(cron_component_dict)

    # highest end of range is non-inclusive
    expected_interpretation = {'MINUTE': [i for i in range(0, 60)], 'HOUR': [i for i in range(0, 24)], 'DAY_OF_MONTH': [
        i for i in range(1, 32)], 'MONTH': [i for i in range(1, 13)], 'DAY_OF_WEEK': [i for i in range(0, 7)], 'COMMAND': ''}
    assert interpreted == expected_interpretation


def test__interpretor_wildcard_with_division():
    cron_component_dict = {
        MINUTE: "*/10",
        HOUR: "*/4",
        DAY_OF_MONTH: "*/5",
        MONTH: "*/4",
        DAY_OF_WEEK: "*/3",
        COMMAND: ""
    }
    interpreted1 = cron_parser._interpret(cron_component_dict)

    # highest end of range is non-inclusive
    expected_interpretation1 = {'MINUTE': [0, 10, 20, 30, 40, 50], 'HOUR': [0, 4, 8, 12, 16, 20], 'DAY_OF_MONTH': [
        5, 10, 15, 20, 25, 30], 'MONTH': [4, 8, 12], 'DAY_OF_WEEK': [0, 3, 6], 'COMMAND': ''}
    assert interpreted1 == expected_interpretation1

    cron_component_dict = {
        MINUTE: "*/11",
        HOUR: "*/3",
        DAY_OF_MONTH: "*/6",
        MONTH: "*/5",
        DAY_OF_WEEK: "*/4",
        COMMAND: ""
    }
    interpreted2 = cron_parser._interpret(cron_component_dict)

    # highest end of range is non-inclusive
    expected_interpretation2 = {'MINUTE': [0, 11, 22, 33, 44, 55], 'HOUR': [0, 3, 6, 9, 12, 15, 18, 21], 'DAY_OF_MONTH': [
        6, 12, 18, 24, 30], 'MONTH': [5, 10], 'DAY_OF_WEEK': [0, 4], 'COMMAND': ''}
    assert interpreted2 == expected_interpretation2


def test__interpretor_range_with_division():
    cron_component_dict = {
        MINUTE: "0-20/3",
        HOUR: "0-13/5",
        DAY_OF_MONTH: "1-20/3",
        MONTH: "1-10/5",
        DAY_OF_WEEK: "0-4/2",
        COMMAND: ""
    }
    interpreted = cron_parser._interpret(cron_component_dict)

    expected_interpretation = {'MINUTE': [0, 3, 6, 9, 12, 15, 18], 'HOUR': [0, 5, 10], 'DAY_OF_MONTH': [
        3, 6, 9, 12, 15, 18], 'MONTH': [5, 10], 'DAY_OF_WEEK': [0, 2, 4], 'COMMAND': ''}
    assert interpreted == expected_interpretation


def test__interpretor_comma():
    cron_component_dict = {
        MINUTE: "0,1,2,59",
        HOUR: "0,1,23",
        DAY_OF_MONTH: "1,2,30,31",
        MONTH: "1,12",
        DAY_OF_WEEK: "0,1,6",
        COMMAND: ""
    }
    interpreted = cron_parser._interpret(cron_component_dict)

    expected_interpretation = {'MINUTE': [0, 1, 2, 59], 'HOUR': [0, 1, 23], 'DAY_OF_MONTH': [
        1, 2, 30, 31], 'MONTH': [1, 12], 'DAY_OF_WEEK': [0, 1, 6], 'COMMAND': ''}
    assert interpreted == expected_interpretation
