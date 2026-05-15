import subprocess
from subprocess import Popen

from muxkit.models import Media, RemuxBackend
from muxkit.backend import FFMpegBackend

class Remuxer:
    """
    Class to handle the remuxing process.
    """

    def __init__(self, backend: RemuxBackend = FFMpegBackend(), dry: bool = False, logFile: str = 'remux.log'):
        self.__logFile: str = logFile
        self.__backend: RemuxBackend = backend
        self.__dry: bool = dry

        # Initialize log file
        with open(self.__logFile, 'w') as f:
            f.write('-------------- Remuxer log file --------------\n\n\n')

    def remux(self, media: Media):
        """
        Remux a single media file.

        :param media: Media object containing video and subtitles to remux.
        """
        
        with open(self.__logFile, 'a') as logFile:
            command: list[str] = self.__compileCommand(media)

            logFile.write(f'Running command: { ' '.join(command) }\n')

            if self.__dry:
                logFile.write('Dry run, not executing command.\n')
                print(f'Dry run, not executing command:\n{" ".join(command)}\n')
                return

            # Flush logfile before running subprocess
            logFile.flush()

            self.__runSubprocess(command, logFile)
            logFile.write('Remuxing completed.\n')

    def remuxBatch(self, mediaList: list[Media]):
        """
        Remux a list of media files. Batch processing.
        Uses multiple processes if possible.

        :param mediaList: List of Media objects to remux.
        """
        #TODO: Implement batch remuxing logic here

        with open(self.__logFile, 'a') as logFile:
            pass
        pass

    def __compileCommand(self, media: Media) -> list[str]:
        """
        Compile the remuxing command using the backend.

        :param media: Media object containing video and subtitles to remux.
        :return: List of command arguments for the remuxing tool.
        """
        return self.__backend.compileMuxCommand(media)

    def __runSubprocess(self, command: list[str], logFile = None):
        """
        Run a subprocess with the given command, wait for it to complete.

        :param command: Command to run as a list of strings.
        :param logFile: Optional open file handle to redirect stdout and stderr.
        """
        subprocess.run(command, stdout=logFile, stderr=logFile)

    def __startSubprocess(self, command: list[str], logFile = None) -> Popen:
        """
        Start a subprocess with the given command, and return the process handle.

        :param command: Command to run as a list of strings.
        :param logFile: Optional open file handle to redirect stdout and stderr.
        """
        return subprocess.Popen(command, stdout=logFile, stderr=logFile)
