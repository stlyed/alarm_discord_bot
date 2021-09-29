#!/usr/bin/env python3

import datetime


def convert_time_24h(time, message):
    # check to see that time is a number not a letter
    # or that hour is under 24 and minute is under 60
    if (time[:2].isdigit() and time[3:].isdigit()) \
            and (int(time[:2]) <= 24) and (int(time[3:]) <= 59):

        # check if user specified afternoon (capital or non capital)
        # and user didn't write time in 24 hour format
        if ((int(time[:2]) <= 12 and message.find('pm', 10, 20) > 0)
                or (int(time[:2]) <= 12 and message.find('PM', 10, 20) > 0)):
            # convert time into 24 hour format
            temp_time = str(time[2:])
            time = int(time[:2]) + 12
            time = str(time) + temp_time

        # if 24 hour is, than make it equal to 00
        if int(time[:2]) == 24:
            time = f'00{time[2:]}'

        # give back time in 24 hour format
        return time
    else:
        # alarm is not verified
        return False


def convert_time_12h(time):
    hour = int(time[:2])
    if hour == 00:
        time = f'12:{time[3:]} AM'
    elif hour == 12:
        time += ' PM'
    elif hour < 12:
        time = f'{time} AM'
    elif hour > 12:
        time = f'0{hour-12}:{time[3:]} PM'
    return time


def verify_date(user_date, time):
    # extract the necessary values from the time also check if they are numbers
    month = user_date[:2]
    day = user_date[3:5]
    year = user_date[6:10]

    current_date = datetime.date.today().strftime("%m-%d-%Y")  # get the current date
    current_time = str(datetime.datetime.now().time())[:5]  # get the current time

    # check if user input are numbers
    if not (str(month).isdigit() or str(day).isdigit() or str(year).isdigit()):
        return False

    # if month is greater than 12
    if not (0 < int(month) <= 12):
        return False

    # allow up 29 days if month is February
    if 0 < int(day) <= 29 and int(month) == 2:
        pass
    # allow up 30 days if an odd month
    elif 0 < int(day) <= 30 and int(month) % 2 == 1:
        pass
    # allow up to 31 days if an even month and it's not February
    elif 0 < int(day) <= 31 and int(month) % 2 == 0 and int(month) != 2:
        pass
    else:
        return False

    # if year does not have 4 characters
    if len(str(year)) != 4:
        return False

    # if user specified date is not in the past
    if not (user_date > current_date
            or (user_date == current_date and time > current_time)):
        return False

    # if function is not false, then nothing happens and return true
    return True

