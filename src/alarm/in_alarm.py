'''
This is a file that runs every 29 seconds as soon as the bot starts
if the current time matches an entry in the saved alarms file
it will notify the users and than delete that entry from the saved alarms file
'''

import datetime
import os
import csv

import variables


def in_alarm():
    # set a default value for alarm
    alarm = 'None'

    # get today's date and current time
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")  # format time
    today = now.strftime("%m-%d-%Y")  # current date, already formmatted
    # get where the files is saved
    file_path = variables.active_alarms_file
    other_file_path = variables.active_alarms_dup_file

    # have 2 file setup: copy to the dup file, delete the main file, rename dup file as main, create dup file
    with open(file_path) as file, open(other_file_path, 'a+', newline='') as other_file:
        reader = csv.reader(file)
        writer = csv.writer(other_file)
        x = True

        for row in reader:
            # if there is an alarm, create the syntax to send out to the user
            if today in row and current_time in row and x:
                alarm = f'{row[0]} your alarm has triggered.\n'

                # if the user specified a name for the alarm then say it
                if '<@' not in row[2]:
                    alarm = f'{alarm[:alarm.find("rm") + 3]} for \"{row[2]}\" {alarm[alarm.find("has") + 3:]}'
                # if the user added any pings than also tell them
                if len(row) == 5: alarm += f'{row[4]}.\n '

                # this is here to make sure that the program grabs one alarm at a time
                x = False

            # copy to dup file only if the row is not currently an alarm
            else:
                writer.writerow(row)

    # recreate 2 file setup
    os.remove(file_path)  # delete main file
    os.rename(other_file_path, file_path)  # rename dup file as main
    file = open(other_file_path, 'w')  # create the dup file
    file.close()

    return alarm
