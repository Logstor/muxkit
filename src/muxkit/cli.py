import sys
import re as regex

from muxkit.models import Media, Subtitle, Video, ProgramOptions, ContentType, Command
from muxkit.remux import Remuxer
from muxkit.matcher import MediaMatcher, MediaMatcherFactory
from muxkit.files import FileList, VideoFactory

def determineLanguageFromFilename(filename: str) -> tuple[str, str] | None:
    """
    Determine the language code and title from a subtitle filename using simple heuristics.

    If no language can be determined, returns None indicating undetermined language.

    :param filename: Filename of the subtitle file.
    :return: Tuple containing the language code and title. E.g., ('eng', 'English').
    """

    # Simple heuristic based on common language codes in filenames
    languageMap = {
        'English': ['eng', regex.compile(r'(\.|-)(eng|english)\.', regex.IGNORECASE)],
        'Danish': ['dan', regex.compile(r'(\.|-)(dan|danish)\.', regex.IGNORECASE)],
        'Spanish': ['spa', regex.compile(r'(\.|-)(spa|spanish)\.', regex.IGNORECASE)],
        'French': ['fra', regex.compile(r'(\.|-)(fra|french)\.', regex.IGNORECASE)],
        'German': ['deu', regex.compile(r'(\.|-)(deu|german)\.', regex.IGNORECASE)],
        'Italian': ['ita', regex.compile(r'(\.|-)(ita|italian)\.', regex.IGNORECASE)],
        'Japanese': ['jpn', regex.compile(r'(\.|-)(jpn|japanese)\.', regex.IGNORECASE)],
        'Chinese': ['chi', regex.compile(r'(\.|-)(chi|chinese)\.', regex.IGNORECASE)],
        'Korean': ['kor', regex.compile(r'(\.|-)(kor|korean)\.', regex.IGNORECASE)],
        # Add more languages as needed
    }

    # Check each language pattern against the filename
    for lang, (code, pattern) in languageMap.items():
        if pattern.search(filename):
            return (code, lang)

    # If no language could be determined, return None
    return None

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
        return '''Usage: muxkit [command] [options] [--help]
Command:
    mux                 Remux video files with their corresponding subtitle files.
    strip               Strip audio and subtitle tracks from video files.
Options:
    --type <movie|show>   Set the content type. Default is 'show'.
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
        # Guard against empty arguments
        if not args or args[0] not in ['mux', 'strip']:
            raise ValueError('No command provided. Expected "mux" or "strip". Use --help for usage information.')


        options: ProgramOptions = ProgramOptions()

        # First parse the command 
        options.command = Command.fromString(args[0])

        i: int = 1
        while i < len(args):
            arg: str = args[i]

            match arg:
                case '--type':
                    if i + 1 < len(args):
                        options.contentType = ContentType.fromString(args[i + 1])
                        i += 2
                    else:
                        raise ValueError('Expected content type after --type')

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
    
def main():
    print('Hello world!')

    # Parse command line arguments
    args: list[str] = sys.argv[1:]

    # Parse arguments into options
    options: ProgramOptions = ProgramArgsParser.parse(args)

    # Check if help is requested
    if options.printHelp:
        print(ProgramArgsParser.helpString())
        return

    print(f'\n{ options.makeArgString() }\n')

    remuxer: Remuxer = Remuxer(dry=options.dry, logFile=options.logFile)

    fileList: FileList = FileList.fromDirectory('.')
    mkvFiles: FileList = fileList.getFilesWithExtension('mkv')
    srtFiles: FileList = fileList.getFilesWithExtension('srt')

    print('MKV Files:')
    for mkv in mkvFiles.getFiles():
        print(f' - { mkv }')

    print('SRT Files:')
    for srt in srtFiles.getFiles():
        print(f' - { srt }')

    # Make Subtitle objects from the SRT files
    subtitles: list[Subtitle] = []
    for sub in srtFiles:
        langInfo = determineLanguageFromFilename(sub)

        # If language could be determined, create a Subtitle object
        if langInfo is not None:
            code, title = langInfo
            subtitles.append(Subtitle(title=title, language=code, filename=sub, path=sub))
            
        # If language could not be determined ask the user
        else:
            print(f'Could not determine language for subtitle file:\n{ sub }')
            langCode: str = input('Language code: ')
            langTitle: str = input('Language title: ')
            subtitles.append(Subtitle(title=langTitle, language=langCode, filename=sub, path=sub))

    print('Subtitles:')
    for sub in subtitles:
        print(f' - {sub}')

    # Make Video objects from the MKV files
    videoFactory: VideoFactory = VideoFactory()
    videoList: list[Video] = videoFactory.fromFileList(mkvFiles)
    print('Videos:')
    [ print(video) for video in videoList ]

    # Match videos with subtitles
    mediaMatcher: MediaMatcher = MediaMatcherFactory.create(options)
    mediaList: list[Media] = mediaMatcher.match(videoList, subtitles)

    # Print matched media
    print('Matched Media:')
    [ print(media) for media in mediaList ]

    print('Do you want to proceed with remuxing? (y/N)')
    proceed: str = input().strip().lower()
    if proceed != 'y':
        print('Aborting remuxing.')
        return

    # Remux each media
    for media in mediaList:
        # Remux
        remuxer.remux(media)

        # Notify done
        print(f'{ media.video.filename } Done')

    print('Remuxing done')
