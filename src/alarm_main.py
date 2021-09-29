#!/usr/bin/env python3
"""
This is the main file for all user request/commands relating alarms
it gets the alarm command and sends to the proper file to get process
Get the processed result and send back to user
"""
import alarm_class


def alarm(author, message):
    alarm_confirmation = ''

    # give help if the command is the only thing typed
    if message == '!alarm':
        alarm_confirmation = 'For help, type !help'

    # create new alarm
    elif '!alarm -set' in message[:11]:
        # !alarm -set will show format if type alone
        if message == '!alarm -set':
            alarm_confirmation = '[hh:mm] [mm-dd-yyyy] ["Alarm Name"] [Mention] \n' \
                                 'only [hh:mm] is mandatory; "Alarm Name" must be in double quotes'
        # attempt to create an alarm and upload it to the database if there are characters after !alarm -set
        else:
            alarm_confirmation = alarm_class.Alarm(message=message, author=author).upload_to_db()[0]

    # see alarms that are currently set
    elif '!alarm -view' in message[:12]:
        # view every message that you have set
        if message == '!alarm -view':
            for i in alarm_class.Alarm().retrieve_from_db():
                alarm_confirmation += f'{i}\n' if i["Author"] == author else ''
            # tell the user if there is no alarm in the database if there aren't any
            if alarm_confirmation == '':
                alarm_confirmation = 'There are currently no alarms in the database that you\'ve created.'

        # view every message in the database
        elif message == '!alarm -view all':
            for i in alarm_class.Alarm().retrieve_from_db():
                alarm_confirmation += f'{i}\n'
            # tell the user if there is no alarm in the database if there aren't any
            if alarm_confirmation == '':
                alarm_confirmation = 'There are currently no alarms in the database.'

    return alarm_confirmation
