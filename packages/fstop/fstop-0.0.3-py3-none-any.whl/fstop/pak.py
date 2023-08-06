from zipfile import ZipFile, ZIP_DEFLATED
import os
import io


class Pak(ZipFile):
    def __init__(self, file):
        try:
            if os.path.isfile(file):
                ZipFile.__init__(self, file, 'a')
            else:
                ZipFile.__init__(self, file, 'x')

            self.file = file

        except Exception as e:
            print('An error occurred opening file:\n%s' % e)

    def add(self, files):
        try:
            if isinstance(files, list):
                for file in files:
                    self.write(os.path.basename(file), compress_type=ZIP_DEFLATED)
            else:
                self.write(files, compress_type=ZIP_DEFLATED)
        except Exception as e:
            print('An error occurred while adding file to PAK file:\n%s' % e)

    def remove(self, files, **kwargs):
        try:
            new_files = []

            if files == 'all':
                if 'except' in kwargs:
                    for file in self.namelist():
                        if file.split('.')[1] == kwargs['except']:
                            new_files.append(file)
                        else:
                            pass
                else:
                    pass
            elif isinstance(files, list):
                for file in self.namelist():
                    if file in files:
                        pass
                    else:
                        new_files.append(file)
            else:
                for file in self.namelist():
                    if file != files:
                        new_files.append(file)

            self.close()
            os.remove(self.file)
            ZipFile.__init__(self, self.file, 'w')

            for file in new_files:
                self.write(file, compress_type=ZIP_DEFLATED)

        except Exception as e:
            print('An error occurred while removing file from PAK file:\n%s' % e)

    def list(self):
        try:
            return self.namelist()
        except Exception as e:
            print('An error occurred while fetching namelist:\n%s' % e)

    def read_file(self, filename, path=''):
        return io.BytesIO(self.read(filename, path))

    def add_resource(self):
        pass
