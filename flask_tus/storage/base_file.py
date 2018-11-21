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

    def delete(self):
        raise NotImplementedError

    def closed(self):
        return not self.file or self.file.closed
