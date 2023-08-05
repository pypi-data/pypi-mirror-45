from distutils.core import setup
setup(
  name = 'FolderUnpacker',         # How you named your package folder (MyLib)
  packages = ['Unpack'],   # Chose the same as "name"
  version = '1.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple python program that extracts all the files from a directory. (Not including folders)',   # Give a short description about your library
  author = 'Daj Katal',                   # Type in your name
  author_email = 'dajkatal@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/dajkatal/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dajkatal/Folder-Unpacker',    # I explain this later on
  keywords = ['Unpacker', 'File Unpacker'],   # Keywords that define your package best
  classifiers=[
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
