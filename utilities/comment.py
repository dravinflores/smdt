###############################################################################
#   File: cleanup.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 May, 2021
#
#   Purpose: This simple script just wipes the new_data and the locks directory.
#   Crashed or prematurely ended programs can leave data here that can mess with things.
#   This should only be ran while developing, this can and will cause data to not get put into the database.
#   DO NOT RUN THIS FILE IN THE REAL LAB IF YOU KNOW WHAT YOU'RE DOING!!!!!
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


import os
import sys

DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

from sMDT import db, tube


def YN_answer_loop(string):
    """
    Gets a yes/no response from the user. Returns true if yes.
    """
    answer = ""
    answer = input(string)
    while answer.lower() not in ['y', 'n']:
        print("Answer not of the form (Y/N).")
        answer = input(string)
    return answer.lower() == 'y'


if __name__ == "__main__":
    database = db.db()
    tubeID = input("Which tube would you like to comment on?\n")
    try:
        tube1 = database.get_tube(tubeID)
        print()
        print(tube1)
        if YN_answer_loop("Would you like to add a comment to this tube? (Y/N)\n"):
            comment = input("What is your comment?\n")
            if YN_answer_loop("Would you still like to add the above comment to the tube? (Y/N)\n"):
                tube2 = tube.Tube()
                tube2.set_ID(tubeID)
                if YN_answer_loop("Does this comment mean the tube is a failure? (Y/N)\n"):
                    tube2.comment_fail = True
                user = input("Enter your name:\n")
                tube2.new_comment((comment, user))
                database.add_tube(tube2)

                input("Comment added.\nPress enter to continue...")
            else:
                input("\nPress enter to continue...")
        else:
            input("\nPress enter to continue...")


    except KeyError:
        input("No tube with that ID found.\nPress enter to continue...")
