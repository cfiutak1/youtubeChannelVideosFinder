import requests
import json
import sys
import date_utils


class ChannelNotFoundException(Exception):
    pass


class MultipleChannelsFoundException(Exception):
    pass


class InvalidDateRangeException(Exception):
    pass


class YoutubeAccessor:
    def __init__(self, api_key, logger):
        self.api_key = api_key
        self.logger = logger
        
    def get_channel_id(self, channel_name):
        self.logger.info("Searching channel id for channel: %s", channel_name)

        # TODO make these formatted strings
        youtube_api_url = "https://www.googleapis.com/youtube/v3/"
        youtube_channels_api_url = youtube_api_url + "channels?key={0}&".format(self.api_key)
        youtube_search_api_url = youtube_api_url + "search?key={0}&".format(self.api_key)

        request_parameters_channel_id = youtube_channels_api_url + "forUsername={0}&part=id"

        try:
            url = request_parameters_channel_id.format(channel_name)
            self.logger.debug("Request: %s", url)

            self.logger.debug("Sending request")
            response = requests.get(url)

        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            sys.exit(1)

        self.logger.debug("Parsing the response")
        response_json = json.loads(response.content)
        self.logger.debug("Response: %s", json.dumps(response_json, indent=4))

        self.logger.debug("Extracting the channel id")
        num_results = response_json["pageInfo"]["totalResults"]

        if num_results > 1:
            self.logger.debug(
                "Multiple channels were received in the response. "
                "If this happens, something can probably be improved around here"
            )
            raise MultipleChannelsFoundException(
                "Multiple channels were received in the response. Try using the channel ID."
            )

        elif num_results == 0:
            self.logger.error("Channel id not found")
            raise ChannelNotFoundException(
                "The channel id could not be retrieved. Make sure that the channel name is correct"
            )

        channel_id = response_json["items"][0]["id"]
        self.logger.info("Channel id found: %s", str(channel_id))

        return channel_id

    def get_channel_videos_in_date_range(self, channel_id, published_before, published_after):
        self.logger.info("Getting videos published before %s and after %s", published_before, published_after)
        
        videos = []
        found_all_videos = False

        next_page_token = ""

        # Strings
        youtube_api_url = "https://www.googleapis.com/youtube/v3/"
        youtube_search_api_url = youtube_api_url + "search?key={0}&".format(self.api_key)

        request_channel_videos_info = youtube_search_api_url + "channelId={0}&part=id&order=date&type=video&publishedBefore={1}&publishedAfter={2}&pageToken={3}&maxResults=50"

        while not found_all_videos:
            url = request_channel_videos_info.format(channel_id, published_before, published_after, next_page_token)
            self.logger.debug("Request: %s", url)

            try:
                response = requests.get(url)

            except requests.exceptions.RequestException as e:
                self.logger.debug(e)
                sys.exit(1)

            self.logger.debug("Parsing the response")
            response_json = json.loads(response.content)

            returned_videos = response_json["items"]
            self.logger.debug("Response: %s", json.dumps(returned_videos, indent=4))

            videos += returned_videos

            if "nextPageToken" in response_json:
                next_page_token = response_json["nextPageToken"]
                self.logger.info("More videos to load, continuing")
                
            else:
                self.logger.info("No more videos to load")
                found_all_videos = True

        self.logger.info("Found %d video(s) in this time interval", len(videos))
        
        return videos

    def get_channel_videos(self, channel_id, date_to_start_from, date_to_go_back_to, time_interval):
        self.logger.info(
            "Searching for videos published in channel between %s and %s", date_to_start_from, date_to_go_back_to
        )
        
        if date_to_start_from < date_to_go_back_to:
            raise InvalidDateRangeException("The date to start from cannot be before the date to go back to!")

        videos = []

        start_date_iter = date_to_start_from
        end_date_iter = start_date_iter - time_interval

        while start_date_iter > date_to_go_back_to:
            if end_date_iter <= date_to_go_back_to:
                self.logger.debug(
                    "The interval is now larger than the remaining time span to retrieve videos for. "
                    "Using the date to go back to as next boundary"
                )
                end_date_iter = date_to_go_back_to

            self.logger.debug("Converting timestamps to RFC3339 format")

            start_date_iter_rfc3339 = date_utils.datetime_to_rfc3339_string(start_date_iter)
            end_date_iter_rfc3339 = date_utils.datetime_to_rfc3339_string(end_date_iter)

            self.logger.debug("\tStart date: " + start_date_iter_rfc3339)
            self.logger.debug("\tEnd date: " + end_date_iter_rfc3339)

            videos_in_interval = self.get_channel_videos_in_date_range(
                channel_id,
                start_date_iter_rfc3339,
                end_date_iter_rfc3339
            )

            videos += videos_in_interval
            self.logger.debug("Total video(s) found so far: %d", len(videos))

            start_date_iter = end_date_iter
            end_date_iter -= time_interval

        self.logger.info("Found %d video(s) in total", len(videos))

        return videos
