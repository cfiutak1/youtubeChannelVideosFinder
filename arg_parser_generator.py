import argparse


class ArgParserGenerator:
    @staticmethod
    def add_api_key_arg(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-k", "--api-key",
            dest="api_key",
            action="store",
            required=True,
            help="Google Data API key to use. You can get one here: https://console.developers.google.com"
        )

        return arg_parser

    @staticmethod
    def add_channel_id_arg(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-c", "--channel_id",
            dest="channel_id",
            action="store",
            required=True,
            help="Youtube channel to get videos from"
        )
        return arg_parser

    @staticmethod
    def add_output_file_path_arg(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-o", "--output-file-path",
            dest="output_file_path",
            action="store",
            default="",
            help="File to write found video links to (content replaced each time). If this option is not specified, "
                 "the links are sent to the standard output "
        )
        return arg_parser

    @staticmethod
    def add_log_file_path_arg(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-l", "--log-file-path",
            dest="log_file_path",
            action="store",
            help="File to write the logs to (content replaced each time). If this option is not specified, the logs "
                 "are sent to the standard output (according to the verbosity level) "
        )
        return arg_parser

    @staticmethod
    def add_date_range_args(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-x", "--date-from",
            dest="date_from",
            action="store",
            help="Videos published after this date will not be retrieved (expected format: yyyy-mm-dd). If not "
                 "specified, the current date is taken "
        )
        arg_parser.add_argument(
            "-y", "--date-to",
            dest="date_to",
            action="store",
            help="Videos published before this date will not be retrieved (expected format: yyyy-mm-dd). If not "
                 "specified, we go back one month (related to -b / --date-from) "
        )
        return arg_parser

    @staticmethod
    def add_interval_arg(arg_parser: argparse.ArgumentParser):
        arg_parser.add_argument(
            "-i", "--interval",
            dest="interval",
            action="store",
            help="Longest period of time (in days) to retrieve videos at a time for. Since the Youtube API only "
                 "permits to retrieve 500 results, the interval cannot be too big, otherwise we might hit the limit. "
                 "Default: 30 days "
        )
        return arg_parser

    @staticmethod
    def add_output_detail_args(arg_parser: argparse.ArgumentParser):
        output_detail_level = arg_parser.add_mutually_exclusive_group()
        output_detail_level.add_argument(
            "-q", "--quiet",
            dest="quiet",
            action="store_true",
            default=False,
            help="Only print out results.. or fatal errors"
        )
        output_detail_level.add_argument(
            "-v", "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
            help="Print out detailed information during execution (e.g., invoked URLs, ...)"
        )
        output_detail_level.add_argument(
            "-d", "--debug",
            dest="debug",
            action="store_true",
            default=False,
            help="Print out all the gory details"
        )
        return arg_parser

    @staticmethod
    def generate_parser():
        arg_parser = argparse.ArgumentParser(
            description="This program finds all videos in a given Youtube channel"
        )
        arg_parser = ArgParserGenerator.add_api_key_arg(arg_parser)
        arg_parser = ArgParserGenerator.add_output_file_path_arg(arg_parser)
        arg_parser = ArgParserGenerator.add_log_file_path_arg(arg_parser)
        arg_parser = ArgParserGenerator.add_date_range_args(arg_parser)
        arg_parser = ArgParserGenerator.add_interval_arg(arg_parser)
        arg_parser = ArgParserGenerator.add_output_detail_args(arg_parser)

        return arg_parser
