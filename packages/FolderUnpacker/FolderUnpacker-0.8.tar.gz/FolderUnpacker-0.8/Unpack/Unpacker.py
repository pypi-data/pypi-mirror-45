import shutil
from os import listdir
from os.path import isfile, join, isdir

desktop_path = '/Users/dajkatal/Desktop'

input_path = desktop_path + '/Static Files/'
output_path = desktop_path + '/Test/'


class FileUnpack(object):
    def __init__(self, input_dir, output_dir):
        self.input = input_dir if input_dir[-1] == '/' else input_dir + '/'
        self.output = output_dir if output_dir[-1] == '/' else output_dir + '/'
        try:
            self.onlyfiles = [input_dir + f for f in listdir(input_dir) if isfile(join(input_dir, f))]
            self.onlydir = [input_dir + f for f in listdir(input_dir) if isdir(join(input_dir, f))]
        except FileNotFoundError as e:
            print('Please check your file paths again, there is not such file as {}'.format(str(e)[str(e).find("'"):]))
            exit()

    def unpack(self):

        try:
            for file in self.onlyfiles:
                shutil.copy(file, self.output)

            def unpack_files(dir_path):
                directories_here = [dir_path + '/' + f for f in listdir(dir_path) if isdir(join(dir_path, f))]
                files_here = [dir_path + '/' + f for f in listdir(dir_path) if isfile(join(dir_path, f))]
                for file in files_here:
                    shutil.copy(file, self.output)
                if len(directories_here) > 0:
                    for dir in directories_here:
                        unpack_files(dir)

            for directory in self.onlydir:
                unpack_files(directory)
            print('Files Successfully Unpacked')
        except FileNotFoundError as e:
            print('Please check your file paths again, there is not such file as {}'.format(str(e)[str(e).find("'"):]))
            exit()


files_init = FileUnpack(input_path, output_path)
files_init.unpack()

