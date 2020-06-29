import os

from .base_file import BaseFile


class FileWrapper(BaseFile):
    """
        Implemenation of appendable and deletable file as a context manager
    """

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs

    def __enter__(self):
        try:
            # Return actual file object, so we dont have to worry about proxying
            self.file = open(self.path, **self.kwargs)
            return self.file        
        except OSError:
            raise

    def __exit__(self, *args, **kwargs):
        self.file.close()

    def delete(self):
        try:
            if self.file:
                # Close file before deleting (Otherwise Windows throws exception )
                self.file.close()
            if os.path.exists(self.path):
                os.remove(self.path)
        except OSError:
            raise

    def append_chunk(self, chunk):
        try:
            with open(self.path, mode='ab') as f:
                f.write(chunk)
        except OSError:
            raise
