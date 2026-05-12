from abc import ABC, abstractmethod
import re as regex
from re import Pattern, Match

from muxkit.models import Subtitle, Video, Media
from muxkit.cli import ProgramOptions, ProgramMode

class MediaMatcher(ABC):
    """
    Video and subtitle matcher based on regex patterns.
    """

    def __init__(self):
        """
        Initialize the MediaMatcher with a regex pattern for matching media files.

        If no pattern is provided, a default pattern is used.

        :param matchPattern: Regex pattern to match media files.
        """
        pass
    
    @abstractmethod
    def match(self, videoList: list[Video], subtitleList: list[Subtitle]) -> list[Media]:
        """
        Match videos with their corresponding subtitles based on the regex pattern.

        :param videoList: List of Video objects.
        :param subtitleList: List of Subtitle objects.
        :return: List of Media objects with matched videos and subtitles.
        """
        pass

class MovieMatcher(MediaMatcher):
    """
    Matcher for movie files.
    """

    def __init__(self):
        super().__init__()

    def match(self, videoList: list[Video], subtitleList: list[Subtitle]) -> list[Media]:
        """
        Match videos with their corresponding subtitles based on the regex pattern.

        :param videoList: List of Video objects.
        :param subtitleList: List of Subtitle objects.
        :return: List of Media objects with matched videos and subtitles.
        """

        # Only support one video to many subtitles matching for movies
        if len(videoList) != 1:
            raise ValueError(f'MovieMatcher only supports one video file. Got { len(videoList) } files.')

        if len(subtitleList) == 0:
            raise ValueError('No subtitle files provided.')
        
        # Create a new Media object with the single video and all subtitles
        return [Media(video=videoList[0], subtitles=subtitleList, outputFilename=self.__makeMovieFilename(videoList[0]))]

    def __makeMovieFilename(self, video: Video) -> str:
        """
        Make a movie filename from the video.

        It's primarily just removing dots from the original filename.

        :param video: Video object.
        """
        dotCount: int = video.filename.count('.')

        if dotCount <= 1:
            return video.filename
        else:
            return video.filename.replace('.', ' ', dotCount - 1)

class TVShowMatcher(MediaMatcher):
    """
    Matcher for TV show files.
    """

    DEFAULT_TV_SHOW_PATTERN: str    = r'S(?P<season>\d{2})E(?P<episode>\d{2}).*?\.(?:mkv|mp4|srt)$'

    def __init__(self, matchPattern: str = DEFAULT_TV_SHOW_PATTERN):
        """
        Initialize the MediaMatcher with a regex pattern for matching media files.

        If no pattern is provided, a default pattern is used.

        :param matchPattern: Regex pattern to match media files.
        """
        super().__init__()
        self.__pattern: Pattern = regex.compile(matchPattern)

    def match(self, videoList: list[Video], subtitleList: list[Subtitle]) -> list[Media]:
        """
        Match videos with their corresponding subtitles based on the regex pattern.

        :param videoList: List of Video objects.
        :param subtitleList: List of Subtitle objects.
        :return: List of Media objects with matched videos and subtitles.
        """

        mediaList: list[Media] = []

        # Index the subtitles by their season and episode for quick lookup
        subtitleIndex: dict[tuple[int, int], list[Subtitle]] = self.__indexSubtitles(subtitleList)

        # Go through each video and find matching subtitles
        for video in videoList:
            match: Match | None = self.__pattern.search(video.filename)

            # Early continue if no match
            if match is None:
                continue

            # Extract season and episode numbers
            season: str = match.group('season')
            episode: str = match.group('episode')

            # Form the key for subtitle lookup
            key: tuple[int, int] = (int(season), int(episode))

            # Get matching subtitles or an empty list if none found
            matchingSubs: list[Subtitle] = subtitleIndex.get(key, [])

            # Create a new Media object, and append to the media list
            mediaList.append(Media(video=video, subtitles=matchingSubs))

        return mediaList

    def __indexSubtitles(self, subtitles: list[Subtitle]) -> dict[tuple[int, int], list[Subtitle]]:
        """
        Index subtitles by their season and episode numbers.

        :param subtitles: List of Subtitle objects to index.
        :return: Dictionary with keys as (season, episode) tuples and values as lists of Subtitle objects.
        """
        index: dict[tuple[int, int], list[Subtitle]] = {}

        for subtitle in subtitles:
            match: Match | None = self.__pattern.search(subtitle.filename)

            # Early continue if no match
            if match is None:
                continue

            # Extract season and episode numbers
            season: str = match.group('season')
            episode: str = match.group('episode')

            key: tuple[int, int] = (int(season), int(episode))

            if key not in index:
                index[key] = []

            index[key].append(subtitle)

        return index

class MediaMatcherFactory:
    """
    Factory class to create MediaMatcher objects based on program options.
    """

    @staticmethod
    def create(programOptions: ProgramOptions) -> MediaMatcher:
        """
        Create a MediaMatcher object based on the given program options.

        :param programOptions: ProgramOptions object containing the mode and other settings.
        :return: Corresponding MediaMatcher object.
        """
        match programOptions.mode:
            case ProgramMode.MOVIE:
                return MovieMatcher()

            case ProgramMode.TV_SHOW:
                return TVShowMatcher()
            
            case _:
                raise ValueError(f'Unsupported program mode: { programOptions.mode }')
