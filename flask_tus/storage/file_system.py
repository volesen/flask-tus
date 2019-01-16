import os

from .base_file import BaseFile


class FileSystem(BaseFile):
    """File System -interface implementation"""
    name = None
    file = None

    def __init__(self, name, file=None):
        self.name = name
        self.file = file

    def open(self, mode='rb'):
        if not self.closed():
            self.file.seek(0)
        else:
            self.file = open(self.name, mode)

        return self.file

    def close(self):
        if self.file:
            return self.file.close()

    def read(self, chunk_size = 1024):
        return self.file.read(chunk_size)

    def write(self, content):
        return self.file.write(content)

    def seek(self, position):
        return self.file.seek(position)

    def delete(self):
        # Close file before deleting (Otherwise Windows throws exception )
        try:
            self.close()
            os.remove(self.name)
        except OSError:
            # Re-raise exception
            raise
