import argparse
from src.cron_parser import cron_parser
from src.exceptions import InvalidCronFormatException, CronComponentValidationException, InvalidUsageOfSpecialOperators
import logging


def main():
    logging.basicConfig(filename='cron_parser.log', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=0)
    parser = argparse.ArgumentParser()
    parser.add_argument("cron_entry", type=str)

    args = parser.parse_args()
    cron_entry = args.cron_entry

    try:
        cron_parser.parse(cron_entry)
    except InvalidCronFormatException as e:
        logging.error("Invalid Cron Format. Please check the cron string")
        print("Invalid Cron Format. Please check the cron string")
    except CronComponentValidationException as e:
        logging.error(e.message)
        print(e.message)
    except Exception as e:
        logging.error(
            "Unable to parse cron expression. Please check the cron string")
        logging.error(str(e))
        print("Unable to parse cron expression. Please check the cron string")
        print(str(e))


if __name__ == "__main__":
    main()
