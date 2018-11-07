class BaseFile(object):
    ''' Proxy object for file '''

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def seek(self):
        raise NotImplementedError

    @property
    def closed(self):
        return not self.file or self.file.closed


class File(BaseFile):
    """ Wrapper for file objects """

    def __init__(self, name, file=None):
        self.name = name
        self.file = file

    def open(self, mode='rb'):
        """Retrieve the specified file from storage."""
        if not self.closed:
            self.file.seek(0)
        else:
            self.file = open(self.name, mode)

    def close(self):
        self.file.close()

    def write(self, content):
        self.file.write(content)

    def seek(self, position):
        self.file.seek(position)
