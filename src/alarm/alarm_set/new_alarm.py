#!/usr/bin/env python3
import csv
import datetime
import variables


def upload_to_csv(data, alarm_confirmation):
    user_date = data[3]  # user specified date
    user_time = data[1]  # user specified time
    current_date = datetime.date.today().strftime("%m-%d-%Y")  # get the current date
    current_time = str(datetime.datetime.now().time())  # get the current time
    current_time = current_time[:5]  # format current time
    file_path = variables.active_alarms_file  # where the alarms are saved

    with open(file_path, 'r') as file:
        # if this alarm was already created
        for row in file:
            if ','.join(data) in row:
                # convert time back to 12 hour format
                if int(user_time[:2]) > 12: user_time = f'{int(user_time[:2]) - 12}:{user_time[3:]} PM'
                elif int(user_time[:2]) == 12: user_time = f'{user_time} PM'
                # error message for user
                alarm_confirmation = f'Alarm could not be created. ' \
                                     f'An alarm named \"{data[2]}\" was already created for {user_time} on the {user_date} by you!'
                # stop file from continuing and tell user the error
                return alarm_confirmation

    # input to the file if user specified date is not in the past
    # or user date is today and time is not in the past
    if user_date > current_date \
            or (user_date == current_date and user_time > current_time):
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            # make sure that alarm is not in the past
            writer.writerow(data)
    else:
        alarm_confirmation = f'alarm could not be created, ' \
                             f'it\'s likely that \"{user_time}\" on {user_date} has already past.\n' \
                             f'Or {user_date} does\'nt exists.'
    return alarm_confirmation
