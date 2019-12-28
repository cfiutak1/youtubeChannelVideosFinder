import datetime
import sys
import logging
import json

from arg_parser_generator import ArgParserGenerator
from youtube_accessor import YoutubeAccessor
from youtube_accessor import ChannelNotFoundException
from youtube_accessor import MultipleChannelsFoundException
from youtube_accessor import InvalidDateRangeException


def initialize_logger(args):
	logger = logging.getLogger(__name__)

	if args.log_file_path is not None:
		handler = logging.FileHandler(args.log_file_path, "w", encoding=None, delay=True)
	else:
		handler = logging.StreamHandler()

	log_format = "[%(asctime)s] [%(levelname)s] - %(message)s"

	handler.setFormatter(logging.Formatter(log_format))

	logger.addHandler(handler)

	if args.verbose:
		logger.setLevel(level=logging.INFO)
	elif args.debug:
		logger.setLevel(level=logging.DEBUG)
	elif args.quiet:
		logger.setLevel(level=logging.ERROR)
	else:
		logger.setLevel(level=logging.WARN)

	return logger


def initialize_date_range(args, logger):
	logger.debug('Initializing variables')

	if args.date_from is not None:
		date_to_start_from = datetime.datetime.strptime(args.date_from, '%Y-%m-%d')
	else:
		date_to_start_from = datetime.datetime.now()

	logger.info('Date to start from: %s', date_to_start_from)

	if args.date_to is not None:
		date_to_go_back_to = datetime.datetime.strptime(args.date_to, '%Y-%m-%d')
	else:
		date_to_go_back_to = date_to_start_from - datetime.timedelta(weeks=4)

	logger.info('Date to go back to: %s', date_to_go_back_to)

	total_time_period = date_to_start_from - date_to_go_back_to
	logger.info('Total period of time to find videos for: %s', str(total_time_period))

	return date_to_start_from, date_to_go_back_to


def initialize_interval(args, logger):
	if args.interval is not None:
		time_interval = datetime.timedelta(days=int(args.interval))
	else:
		time_interval = datetime.timedelta(weeks=4)

	logger.info("Time interval: %s", time_interval)

	return time_interval


def output_videos_to_file(videos, file_path):
	f = open(file_path, "w")

	json.dump(videos, f, indent=2)

	f.close()


def main():
	parser = ArgParserGenerator.generate_parser()
	args = parser.parse_args()

	log = initialize_logger(args)

	date_to_start_from, date_to_go_back_to = initialize_date_range(args, log)
	interval = initialize_interval(args, log)

	yt_accessor = YoutubeAccessor(args.api_key, log)

	try:
		channel_id = yt_accessor.get_channel_id(args.channel)

	except ChannelNotFoundException or MultipleChannelsFoundException as e:
		print(e)
		sys.exit(1)

	try:
		channel_videos = yt_accessor.get_channel_videos(
			channel_id,
			date_to_start_from,
			date_to_go_back_to,
			interval
		)

	except InvalidDateRangeException as e:
		print(e)
		sys.exit(1)

	if args.output_file_path is None:
		print(channel_videos)
	else:
		output_videos_to_file(channel_videos, args.output_file_path)


if __name__ == "__main__":
	main()
