import os

class cd:
    def __init__(self, dir):
        self.newdir = dir

    def __enter__(self):
        self.olddir = os.getcwd()
        os.chdir(self.newdir)

    def __exit__(self):
        os.chdir(self.olddir)
