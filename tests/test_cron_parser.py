from src.cron_parser import cron_parser


def test_parse_success():
    parsed_output = cron_parser.parse("*/15 0 1,15 * 2-5/2 /usr/bin/find")
    assert parsed_output == "parsed"
