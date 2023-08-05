from zipfile import ZipFile


class Pak(ZipFile):
    def __init__(self, file):
        ZipFile.__init__(self, file)

    def list(self):
        return self.namelist()