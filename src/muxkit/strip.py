from muxkit.models import ProgramOptions, Video
from muxkit.backend import RemuxBackend

class Strip:
    """
    Class responsible for iteractively letting the user strip audio and subtitle tracks/streams
    from video files.
    """

    def __init__(self, backend: RemuxBackend, videoFiles: list[Video], options: ProgramOptions):
        self.backend: RemuxBackend = backend
        self.videoFiles: list[Video] = videoFiles
        self.options: ProgramOptions = options

    def run(self):
        """
        Run the stripping process, interactively asking the user which tracks/streams to strip from each video file.
        """
        cmd = self.backend.compileProbeCommand(self.videoFiles[0])
        print(f'Running probe command: {" ".join(cmd)}')
