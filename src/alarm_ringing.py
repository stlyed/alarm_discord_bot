#!/usr/bin/env python3
import datetime

import alarm_class


def alarm_ringing():
    confirmation = alarm_id = 'None'
    current_date = datetime.date.today().strftime("%m-%d-%Y")  # get the current date
    current_time = str(datetime.datetime.now().time())[:5]  # get the current time

    # retrieve everything from the database
    for i in alarm_class.Alarm().retrieve_from_db():
        # if current date and time match an entre in the database
        if current_date == i['Date'] and current_time == i['Time']:

            # notify the user
            confirmation = f'{i["Author"]} your alarm has triggered.\n'
            # notify the user with custom alarm name
            if i['Author'] != i['Alarm Name']:
                confirmation = f'{i["Author"]} your alarm for \"{i["Alarm Name"]}\" has triggered.\n'
            # add any mentions
            if i["Mention"] != '':
                confirmation += f'{i["Mention"]}, is also being pinged'

            alarm_id = i["Alarm Id"]
            break

    return [confirmation, alarm_id]
