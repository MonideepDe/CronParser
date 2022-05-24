from src.constants import MINUTE, HOUR, DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND


class CronPrettyPrinter:
    def __init__(self) -> None:
        self.key_col_len = 14
        self.key_to_out_col_name = {
            MINUTE: "minute", HOUR: "hour", DAY_OF_MONTH: "DAY_OF_MONTH", MONTH: "MONTH", DAY_OF_WEEK: "DAY_OF_WEEK", COMMAND: "COMMAND"
        }
        self.output_order = [MINUTE, HOUR,
                             DAY_OF_MONTH, MONTH, DAY_OF_WEEK, COMMAND]

    def pretty_print(self, cron_interpreted: dict) -> str:
        out_str_list = []
        for key in self.output_order:
            out_key = self.key_to_out_col_name[key]
            out_val = cron_interpreted[key]
            if isinstance(out_val, list):
                out_val = " ".join([str(i) for i in out_val])
            print("{0:<14}{1}".format(out_key, out_val))
            out_str_list.append("{0:<14}{1}".format(out_key, out_val))
        return "\n\r".join(out_str_list)


cron_pretty_printer = CronPrettyPrinter()
