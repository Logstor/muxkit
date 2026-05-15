from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

@dataclass
class Subtitle:
    """
    Subtitle file with language and title metadata.
    """

    title: str
    """
    Title of the subtitle track. e.g., 'English', 'Spanish'.
    """
    
    language: str
    """
    Language code of the subtitle track. e.g., 'eng', 'spa'.
    """

    path: str
    """
    Full path to the subtitle file.
    """

    filename: str
    """
    Filename of the subtitle file.
    """

    def __str__(self):
        return f'''Subtitle:
            Title: {self.title}
            Language: {self.language}
            Filename: {self.filename}
            '''

@dataclass
class Video:
    """
    Video file.
    """

    title: str
    """
    Title of the video file.
    """

    path: str
    """
    Full path to the video file.
    """

    filename: str
    """
    Filename of the video file.
    """

    def __str__(self):
        return f'''Video:
            Title: {self.title}
            Filename: {self.filename}
            Path: {self.path}
            '''

@dataclass
class Media:
    """
    Video with associated subtitles and metadata.
    """

    video: Video
    """
    Video file.
    """

    subtitles: list[Subtitle]
    """
    List of associated subtitle files.
    """

    outputFilename: str | None = None
    """
    The filename to give to the output file.

    If None is given, then it makes a default with a .mux.mkv ending
    """

    def getOutputFilename(self) -> str:
        """

        """
        if self.outputFilename is not None:
            return self.outputFilename
        else:
            return self.video.filename.replace('.mkv', '.mux.mkv')

    def __str__(self):
        return f'''Media:
            { str(self.video) }
            { ', '.join(str(sub) for sub in self.subtitles) }
        '''

class Command(Enum):
    """
    Enum for commands.
    """
    MUX = 'mux'
    STRIP = 'strip'

    @staticmethod
    def fromString(value: str) -> Command:
        """
        Convert a string to a Command enum value.

        :param value: String representation of the command.
        :return: Corresponding Command enum value.
        """
        match value.lower():
            case 'mux':
                return Command.MUX
            
            case 'strip':
                return Command.STRIP

            case _:
                raise ValueError(f'Invalid command: { value }. Expected "mux" or "strip".')

class ContentType(Enum):
    """
    Enum for content types.
    """
    MOVIE = 'movie'
    TV_SHOW = 'show'

    @staticmethod
    def fromString(value: str) -> ContentType:
        """
        Convert a string to a ContentType enum value.

        :param value: String representation of the content type.
        :return: Corresponding ContentType enum value.
        """
        match value.lower():
            case 'movie':
                return ContentType.MOVIE
            
            case 'show':
                return ContentType.TV_SHOW

            case _:
                raise ValueError(f'Invalid content type: { value }. Expected "movie" or "show".')

@dataclass
class ProgramOptions:
    """
    Class to hold program options, and parse command line arguments.
    """

    printHelp: bool = False
    """
    If True, print help message and exit.
    """

    command: Command = Command.MUX
    """
    Command to execute.
    """

    contentType: ContentType = ContentType.TV_SHOW
    """
    Content type, either MOVIE or TV_SHOW.
    """

    dry: bool = False
    """
    If True, do not actually perform remuxing, just print commands.
    """

    logFile: str = 'remux.log'
    """
    Path to the log file.
    """

    def makeArgString(self) -> str:
        """
        Make a string representation of the current options for logging.

        :return: String representation of options.
        """
        return f'ProgramOptions(command={ self.command }, contentType={ self.contentType }, dry={ self.dry }, logFile="{ self.logFile }")'
