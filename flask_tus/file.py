class BaseFile(object):
    """ Abstract class file definition --Interface"""
    file = None

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def write(self, content):
        raise NotImplementedError

    def seek(self, position):
        raise NotImplementedError

    def closed(self):
        return not self.file or self.file.closed


class File(BaseFile):
    """Interface implementation"""
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
