import argparse
from src.cron_parser import cron_parser


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cron_entry", type=str)

    args = parser.parse_args()
    cron_entry = args.cron_entry

    try:
        cron_parser.parse(cron_entry)
    except Exception as e:
        print("Unable to parse cron expression. Please check the cron string")
        print(str(e))


if __name__ == "__main__":
    main()
