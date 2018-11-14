from .base_file import BaseFile


class File(BaseFile):
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
        return self.file.close()

    def write(self, content):
        return self.file.write(content)

    def seek(self, position):
        return self.file.seek(position)
