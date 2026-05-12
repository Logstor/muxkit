import re as regex
from re import Pattern, Match

from muxkit.models import Video

class FileList:
    """
    Class to manage a list of files.
    """

    def __init__(self):
        self._files = []

    def __iter__(self):
        return iter(self._files)

    def __len__(self):
        return len(self._files)

    def append(self, filename: str):
        self._files.append(filename)

    def getFiles(self) -> list[str]:
        return self._files

    def getFilesWithExtension(self, extension: str | None = None, extensionRegex: str | None = None) -> FileList:
        """
        Get files with a specific extension (case insensitive).

        NOTE: Either extension or extensionRegex must be provided, but not both.

        :param extension: File extension to filter by (e.g., 'mkv', 'srt').
        :param extensionRegex: Regex pattern to filter by (e.g., 'mkv|mp4|avi').
        :return: A new FileList containing files with the specified extension.
        """

        # Check arguments validity
        if (extension is None and extensionRegex is None) or (extension is not None and extensionRegex is not None):
            raise ValueError('Either extension or extensionRegex must be provided, but not both.')

        res: FileList = FileList()

        # Prepare and compile regex pattern for case-insensitive matching
        if extensionRegex is not None:
            pattern: Pattern = regex.compile(f'.*\\.{ extensionRegex }$', regex.IGNORECASE)
        else:
            pattern: Pattern = regex.compile(f'.*\\.{ extension }$', regex.IGNORECASE)

        # Go through all files and match with the pattern
        for file in self._files:
            if pattern.match(file):
                res.append(file)

        # Return the resulting FileList
        return res

    @staticmethod
    def fromDirectory(directory: str) -> FileList:
        """
        Create a FileList from files in a specified directory.

        :param directory: Directory path to scan for files.
        :return: A FileList containing all files in the directory.
        """
        import os

        res: FileList = FileList()

        # List all files in the given directory
        for entry in os.listdir(directory):
            fullPath = os.path.join(directory, entry)
            if os.path.isfile(fullPath):
                res.append(fullPath)

        # Return the populated FileList
        return res

class VideoFactory:
    """
    Factory class to create Video objects from filenames.
    """

    TITLE_PATTERN: str = r'(?P<title>.+?)\.(mkv|mp4|avi)$'
    """
    Regex pattern to extract title from video filename.

    Simple heuristic: everything before the last dot and extension.
    1. title: The title of the video.
    2. extension: The file extension (mkv, mp4, avi).
    3. Case insensitive.
    4. Non-greedy match for title to handle dots in the title.
    """

    def __init__(self):
        self.__title_pattern: Pattern = regex.compile(self.TITLE_PATTERN, regex.IGNORECASE)

    def fromFileList(self, fileList: FileList) -> list[Video]:
        """
        Create Video objects from a FileList.
        """
        videos: list[Video] = []

        for filename in fileList:
            try:
                title = self.__extractTitle(filename)
                videos.append(Video(title=title, filename=filename, path=filename))
            except ValueError as e:
                print(f'Warning: { e }')

        return videos

    def __extractTitle(self, filename: str) -> str:
        """
        Extract the title from a video filename.
        """

        match: Match | None = self.__title_pattern.search(filename)

        if match is None:
            raise ValueError(f'Could not extract title from filename: { filename }')

        return match.group('title').replace('.', ' ')

