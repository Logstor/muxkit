import json
from muxkit.models import RemuxBackend, Media, Video, VideoStreamInfo

class FFMpegBackend(RemuxBackend):
    """
    FFMpeg backend for remuxing.
    """

    FFMPEG_PROGRAM: str = 'ffmpeg'
    FFPROBE_PROGRAM: str = 'ffprobe'

    def parseProbeOutput(self, output: str) -> list[VideoStreamInfo]:
        jsonOutput = json.loads(output)

        return []

    def compileProbeCommand(self, video: Video) -> list[str]:
        return f'{ self.FFPROBE_PROGRAM } -show_streams -print_format json "{ video.path }"'.split()

    def compileStripCommand(self, video: Video, streamIdxToStrip: list[int]) -> list[str]:
        return []

    def compileMuxCommand(self, media: Media) -> list[str]:
        """
        Compile the ffmpeg command for remuxing the given media.

        :param media: Media object containing video and subtitles to remux.
        :return: List of command arguments for ffmpeg.
        """

        # Start with all inputs
        command: list[str] = [ self.FFMPEG_PROGRAM ,'-i', media.video.path ]

        # Add all input subtitles for this media
        for sub in media.subtitles:
            command += [ '-i', sub.path ]

        # All mapping commands coming after inputs
        command += [
            '-map', '0', # Map all streams from the first input (video)
            '-c', 'copy', # Copy all streams without re-encoding
            '-map_chapters', '0', # Copy chapters from the first input
            '-map_metadata', '0', # Copy metadata from the first input
        ]

        #TODO: Probe the video for existing subtitles to avoid overriding existing subtitle metadata
        # ffprobe -v error -select_streams s -show_entries stream=index -of csv=p=0 input.mkv


        # Add mapping for each subtitle
        for index, subtitle in enumerate(media.subtitles):
            command.extend([
                '-map', f'{ index + 1 }:0', # Map the subtitle stream from the corresponding input
                f'-metadata:s:s:{ index }', f'language=\"{ subtitle.language }\"',
                f'-metadata:s:s:{ index }', f'title=\"{ subtitle.title }\"'
            ])

        # Set output format
        command.extend([ '-f', 'matroska' ])

        # Output filename
        command.append(media.getOutputFilename())

        return command
    
    def _parseFFProbeOutput(self) -> list[VideoStreamInfo]:
        """
        Create a list of VideoStreamInfo objects from ffprobe output.
        """
        return []

