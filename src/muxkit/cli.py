from enum import Enum
from dataclasses import dataclass

class ProgramMode(Enum):
    """
    Enum for program modes.
    """
    MOVIE = 'movie'
    TV_SHOW = 'show'

    @staticmethod
    def fromString(value: str) -> ProgramMode:
        """
        Convert a string to a ProgramMode enum value.

        :param value: String representation of the mode.
        :return: Corresponding ProgramMode enum value.
        """
        match value.lower():
            case 'movie':
                return ProgramMode.MOVIE
            
            case 'show':
                return ProgramMode.TV_SHOW

            case _:
                raise ValueError(f'Invalid mode: { value }. Expected "movie" or "show".')

@dataclass
class ProgramOptions:
    """
    Class to hold program options, and parse command line arguments.
    """

    printHelp: bool = False
    """
    If True, print help message and exit.
    """

    mode: ProgramMode = ProgramMode.TV_SHOW
    """
    Program mode, either MOVIE or TV_SHOW.
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
        return f'ProgramOptions(mode={ self.mode }, dry={ self.dry }, logFile="{ self.logFile }")'

class ProgramArgsParser:
    """
    Class to parse command line arguments into ProgramOptions.
    """

    @staticmethod
    def helpString() -> str:
        """
        Return a help string for command line arguments.

        :return: Help string.
        """
        return '''Usage: remuxing.py [options] [--help]
Options:
    --mode <movie|show>   Set the program mode. Default is 'show'.
    --dry                 Perform a dry run without actual remuxing.
    --log <file>          Specify the log file path. Default is 'remux.log'.
    --help                Show this help message and exit.
'''

    @staticmethod
    def parse(args: list[str]) -> ProgramOptions:
        """
        Parse command line arguments and return a ProgramOptions object.

        :param args: List of command line arguments (excluding program name).
        :return: ProgramOptions object with parsed options.
        """
        options: ProgramOptions = ProgramOptions()

        i: int = 0
        while i < len(args):
            arg: str = args[i]

            match arg:
                case '--mode':
                    if i + 1 < len(args):
                        modeStr: str = args[i + 1].lower()
                        if modeStr == 'movie':
                            options.mode = ProgramMode.MOVIE
                        elif modeStr == 'show':
                            options.mode = ProgramMode.TV_SHOW
                        else:
                            raise ValueError(f'Invalid mode: { modeStr }. Expected "movie" or "show".')
                        i += 2
                    else:
                        raise ValueError('Expected mode after --mode')

                case '--dry':
                    options.dry = True
                    i += 1
                    continue

                case '--log':
                    if i + 1 < len(args):
                        options.logFile = args[i + 1]
                        i += 2
                    else:
                        raise ValueError('Expected log file path after --log')

                case '--help':
                    options.printHelp = True
                    break

        return options
