import filecmp
import os
from shutil import copy
import pathlib

dropbox_dir = r'C:\smdt'
github_dir = r'C:\smdt-main'
#dropbox_dir, github_dir = github_dir, dropbox_dir



for subdir, dirs, files in os.walk(dropbox_dir):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".py"):
            print(filepath)
            git_filepath = github_dir + filepath[len(dropbox_dir):]
            if os.path.isfile(git_filepath):
                if filecmp.cmp(git_filepath, filepath, shallow=False):
                    print("Match!")
                else:
                    print("Mismatch!")
            else:
                print("Does not exist in github!")
                try:
                    os.makedirs(github_dir + subdir[len(dropbox_dir):])
                except FileExistsError:
                    pass
                copy(filepath, git_filepath)