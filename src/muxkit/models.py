from dataclasses import dataclass

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
