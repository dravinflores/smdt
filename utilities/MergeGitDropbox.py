###############################################################################
#   File: MergeGitDropbox
#   Author(s): Paul Johnecheck
#   Date Created: 9/12/2021
#
#   Purpose: This script is designed to make it easier to reconcile differences
#   between the dropbox and the github. Currently, it expects a path to the dropbox directory
#   and a path to the local github repository.
#   Uncommenting line 25 will do the reverse, compares them in the opposite direction.
#   This script will be improved further in the future.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


import filecmp
import os
from shutil import copy
import pathlib

dropbox_dir = r'C:\smdt'
github_dir = r'C:\smdt-main'


mode = input("Modes:\n(1): Compare only\n(2): Add missing files to each\n(3): Update from GitHub\n(4): Update from "
             "Dropbox\n")
while mode not in ["1","2","3","4"]:
    mode = input("Please choose a value in Modes [1,2,3,4],\n(1): Compare only\n(2): Add missing files to each\n(3): Update from GitHub\n(4): Update from "
                 "Dropbox\n")
mode = int(mode)

matches = []
mismatches = []
dropbox_only = []
github_only = []


for subdir, dirs, files in os.walk(dropbox_dir):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".py"):# or filepath.endswith(".vi"):
            git_filepath = github_dir + filepath[len(dropbox_dir):]
            if os.path.isfile(git_filepath):
                if filecmp.cmp(git_filepath, filepath, shallow=False):
                    matches.append(filepath)
                else:
                    mismatches.append(filepath)
                    if mode == 3:
                        copy(git_filepath, filepath)
                    elif mode == 4:
                        copy(filepath, git_filepath)
            else:
                dropbox_only.append(filepath)
                if mode == 2:
                    try:
                        os.makedirs(github_dir + subdir[len(dropbox_dir):])
                    except FileExistsError:
                        pass
                    copy(filepath, git_filepath)

for subdir, dirs, files in os.walk(github_dir):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".py"):# or filepath.endswith(".vi"):
            dropbox_filepath = dropbox_dir + filepath[len(github_dir):]
            if not os.path.isfile(dropbox_filepath):
                github_only.append(filepath)
                if mode == 2:
                    try:
                        os.makedirs(dropbox_dir + subdir[len(github_dir):])
                    except FileExistsError:
                        pass
                    copy(filepath, dropbox_filepath)

if matches:
    print("\nComplete Matches:")
    [print(path) for path in matches]
if mismatches:
    print("\nIncomplete Matches:" + (" - Now Complete matches based on the " + ("GitHub" if mode == 3 else "Dropbox") + " version" if mode in [3,4] else ""))
    [print(path) for path in mismatches]
if github_only:
    print("\nOnly on GitHub" + (" - Now added to Dropbox" if mode == 2 else ""))
    [print(path) for path in github_only]
if dropbox_only:
    print("\nOnly on Dropbox" + (" - Now added to GitHub" if mode == 2 else ""))
    [print(path) for path in dropbox_only]