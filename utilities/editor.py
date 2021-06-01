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
import datetime

DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

from sMDT import db, tube


def answer_loop(string, options):
    """
    Gets an answer from the user
    """
    answer = ""
    answer = input(string)
    while answer.lower() not in options:
        print("Lowercase input is not in ", options, ", try again.\n")
        answer = input(string)
    return answer.lower()

def str_now():
    return datetime.datetime.now().strftime("<%Y-%m-%d, %H:%M:%S>: ")



if __name__ == "__main__":
    log_path = "edit.log"

    database = db.db()
    tubeID = input("Enter a tube ID.\n")
    new_tube = False
    log = ""
    try:
        tube1 = database.get_tube(tubeID)
    except KeyError:
        if answer_loop("A tube with that ID was not found. Would you like to create it? [Y/N]\n", ['y', 'n']) == 'y':
            tube1 = tube.Tube()
            tube1.set_ID(tubeID)
            new_tube = True
        else:
            quit()
    while True:
        print()
        print(tube1)
        choice = answer_loop(
            "What would you like to do with this tube?\n[E]dit\n[D]elete\n[S]ave and close\n[C]lose without saving\n",
            ['e', 'd', 's', 'c'])
        if choice == 'e':
            editChoice = answer_loop("How would you like to edit this tube?\n[I]D change\n[C]omments\n[S]tations\n",
                                     ['i', 'c', 's'])
            if editChoice == 'i':
                new_ID = input("What will the tube's new ID be?\n")
                try:
                    database.get_tube(new_ID)
                    print(
                        "WARNING: A tube with the ID you gave already exists. If you continue, data from the above tube will be added to existing data on this tube.")
                except KeyError:
                    pass
                string = "Confirm changing this tube from ID " + str(
                    tube1.get_ID()) + " to " + new_ID + "?\nThis will also delete the tube at it's original ID. [Y/N]\n"
                if answer_loop(string, ['y', 'n']) == 'y':
                    database.delete_tube(tube1)
                    tube1.set_ID(new_ID)
                    database.add_tube(tube1)
                    log += str_now() + "Deleted tube " + str(tubeID) + " and moved its data to tube " + str(new_ID) + '\n'
                    logfile = open(log_path, 'a')
                    logfile.write(tubeID + '\n')
                    logfile.write(log)
                    break

            elif editChoice == 'c':
                commentChoice = answer_loop(
                    "How would you like to edit these comments?\n[A]dd a comment\n[D]elete a comment\n[E]dit a comment\n[I]nvert the comment_fail flag\n",
                    ['i', 'e', 'a', 'd'])
                if commentChoice == 'a': #Add a comment
                    comment = input("What is your comment?\n")
                    if answer_loop("Would you still like to add the above comment to the tube? (Y/N)\n",
                                   ['y', 'n']) == 'y':
                        if answer_loop("Does this comment mean the tube is a failure? (Y/N)\n", ['y', 'n']) == 'y':
                            tube1.comment_fail = True
                        user = input("Enter your name:\n")
                        tube1.new_comment((comment, user, datetime.datetime.now()))
                        log += str_now() + 'Added comment "' + comment + '" to tube ' + '\n'
                elif commentChoice == 'e': #Edit a comment
                    index = input("Enter the 0 index of the comment you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.m_comments):
                            print("Invalid comment index")
                            continue
                        new_comment = input(
                            "You have selected to edit comment " + str(index) + "\n" + tube1.m_comments[index][
                                0] + "\nRewrite the comment now.\n")
                        if answer_loop(
                                "Would you still like to replace the original comment with your new one? (Y/N)\n",
                                ['y', 'n']) == 'y':
                            log += str_now() + 'Replaced comment "' + tube1.m_comments[index][0] + '" with ' + new_comment  + '\n'
                            tube1.m_comments[index][0] = new_comment

                    except ValueError:
                        print("Invalid comment index")
                elif commentChoice == 'd': #Delete a comment
                    index = input("Enter the 0 index of the comment you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.m_comments):
                            print("Invalid comment index")
                            continue
                        comment, user, date = tube1.m_comments[index]
                        print("You have selected to delete comment " + str(
                            index) + "\n" + comment + " -" + user + " " + date.date().isoformat() + '\n')
                        if answer_loop("Would you still like to delete this comment? (Y/N)\n", ['y', 'n']) == 'y':
                            del tube1.m_comments[index]
                            log += str_now() + 'Deleted comment "' + tube1.m_comments[index][0] + '\n'
                            print("Deleted comment")
                    except ValueError:
                        print("Invalid comment index")
                elif commentChoice == 'i': #Invert the comment failure flag
                    if tube1.comment_fail:
                        print("This tube has been previously marked as a failure by a comment.")
                    else:
                        print("This tube has not been previously marked as a failure by a comment.")
                    if answer_loop("Would you like to invert this flag? [Y/N]\n", ['y', 'n']) == 'y':
                        tube1.comment_fail = not tube1.comment_fail
                        log += str_now() + 'Comment fail flag inverted' + '\n'
                        print("Comment fail flag inverted")
            elif editChoice == 's': #Edit the station's data
                stationChoice = answer_loop(
                    "Which station's data would you like to modify?\n[S]wage\n[T]ension\n[L]eak\n[D]ark Current\n",
                    ['s', 't', 'l', 'd'])
                if stationChoice == 's': #Edit the swage station
                    index = input("Enter the 0 index of the record you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.swage.m_records):
                            print("Invalid record index")
                            continue
                        value_choice = answer_loop("You chosen to edit the following record.\n"
                                                   + str(tube1.swage.m_records[index])
                                                   + "\nWhich value would you like to change?"
                                                   + "\n[R]aw_length\n[S]wage_length\n[C]lean_code\n[E]rror_code\n",
                                                   ['r', 's', 'c', 'e'])
                        if value_choice == 'r':
                            new_value = input("Input a new value for raw_length.\n")
                            float(new_value)
                            log += str_now() + "Record " + str(index) + ': Replaced raw length value of ' + str(tube1.swage.m_records[index].raw_length) + " with " + new_value + '\n'
                            tube1.swage.m_records[index].raw_length = float(new_value)

                        if value_choice == 's':
                            new_value = input("Input a new value for swage_length.\n")
                            float(new_value)
                            log += str_now() + "Record " + str(index) + ': Replaced swage length value of ' + str(
                                tube1.swage.m_records[index].swage_length) + " with " + new_value + '\n'
                            tube1.swage.m_records[index].swage_length = float(new_value)
                        if value_choice == 'c':
                            new_value = input("Input a new value for clean_code.\n")
                            log += str_now() + "Record " + str(index) + ': Replaced clean code value of ' + str(
                                tube1.swage.m_records[index].clean_code) + " with " + new_value + '\n'
                            tube1.swage.m_records[index].clean_code = new_value

                        if value_choice == 'e':
                            new_value = input("Input a new value for error code.\n")
                            log += str_now() + "Record " + str(index) + ': Replaced error code value of ' + str(
                                tube1.swage.m_records[index].error_code) + " with " + new_value + '\n'
                            tube1.swage.m_records[index].error_code = new_value
                    except ValueError:
                        print("Invalid input")
                        continue
                if stationChoice == 't': #Edit the tension station
                    index = input("Enter the 0 index of the record you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.tension.m_records):
                            print("Invalid record index")
                            continue
                        value_choice = answer_loop("You chosen to edit the following record.\n"
                                                   + str(tube1.tension.m_records[index])
                                                   + "\nWhich value would you like to change?"
                                                   + "\n[T]ension\n[F]requency\ne",
                                                   ['t', 'f'])
                        if value_choice == 't':
                            new_value = input("Input a new value for tension.")
                            float(new_value)
                            log += str_now() + "Swage Record " + str(index) + ': Replaced tension value of ' + str(
                                tube1.tension.m_records[index].tension) + " with " + new_value + '\n'
                            tube1.tension.m_records[index].tension = float(new_value)

                        if value_choice == 'f':
                            new_value = input("Input a new value for frequency.")
                            float(new_value)
                            log += str_now() + "Tension Record " + str(index) + ': Replaced frequency value of ' + str(
                                tube1.tension.m_records[index].frequency) + " with " + new_value + '\n'
                            tube1.tension.m_records[index].frequency = float(new_value)
                    except ValueError:
                        print("Invalid input")
                        continue
                if stationChoice == 'l': #Edit the leak station
                    index = input("Enter the 0 index of the record you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.leak.m_records):
                            print("Invalid record index")
                            continue
                        print("Only the leak_rate data point may be changed for the leak station.")
                        new_value = input("Input a new value for leak_rate.\n")
                        float(new_value)
                        log += str_now() + "Leak Record " + str(index) + ': Replaced leak_rate value of ' + str(
                            tube1.leak.m_records[index].leak_rate) + " with " + new_value + '\n'
                        tube1.leak.m_records[index].leak = float(new_value)
                    except ValueError:
                        print("Invalid input")
                        continue
                if stationChoice == 'd': #Edit the dark current station
                    index = input("Enter the 0 index of the record you want to edit\n")
                    try:
                        index = int(index)
                        if index >= len(tube1.leak.m_records):
                            print("Invalid record index")
                            continue
                        print("Only the dark_current data point may be changed for the dark current station.")
                        new_value = input("Input a new value for dark_current.\n")
                        float(new_value)
                        log += str_now() + "Dark Current Record " + str(index) + ': Replaced dark_current value of ' + str(
                            tube1.dark_current.m_records[index].dark_current) + " with " + new_value + '\n'
                        tube1.dark_current.m_records[index].dark_current = float(new_value)
                    except ValueError:
                        print("Invalid input")
                        continue


        elif choice == 'd': #delete the tube
            if answer_loop("Are you sure you want to delete tube " + tubeID + "? [Y/N]\n", ['y', 'n']) == 'y':
                database.delete_tube(tube1.get_ID())
                print("Tube marked for deletion, now closing.\n")
                logfile = open(log_path, 'a')
                entry = str_now() + "Deleted tube " + tubeID + '\n'
                logfile.write(entry)
            break
        elif choice == 's': #save and exit
            if new_tube:
                database.add_tube(tube1)
            else:
                database.overwrite_tube(tube1)
            print("Saved, now closing.\n")
            logfile = open(log_path, 'a')
            logfile.write(tubeID)
            logfile.write(log)
            break
        elif choice == 'c': #exit without saving
            print("Closing without saving.\n")
            break
    else:
        input("\nPress enter to continue...")

    input("End of execution.\nPress enter to continue...")
