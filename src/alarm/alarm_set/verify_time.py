#!/usr/bin/env python3
def verify_time(time, message):
    # check to see that time is a number not a letter
    # or that hour is under 24 and minute is under 60
    if (time[:2].isdigit() and time[3:].isdigit()) \
            and (int(time[:2]) <= 24) and (int(time[3:]) <= 59):
        # alarm is verified
        verified = True

        # check if user specified afternoon (capital or non capital)
        # and user didn't write time in 24 hour format
        if ((int(time[:2]) <= 12 and message.find('pm', 10, 20) > 0)
                or (int(time[:2]) <= 12 and message.find('PM', 10, 20) > 0))  \
                and (int(time[:2]) < 12):
            # convert time into 24 hour format
            temp_time = str(time[2:])
            time = int(time[:2]) + 12
            time = str(time) + temp_time

        # tell user what time their alarm is set for
        # if it is less than 12 than just write AM; if not convert to 12 hour and write PM
        alarm_confirmation = f'{time} AM '
        if int(time[:2]) == 12: alarm_confirmation = f'{time} PM '
        elif int(time[:2]) > 12: alarm_confirmation = f'{int(time[:2]) - 12}:{time[3:]} PM '

    else:
        # alarm is not verified
        verified = False

        # tell the user the error message
        alarm_confirmation = f'Your alarm could not be created, ' \
                             f'it\'s likely that \"{time}\" is invalid ' \
                             f'or you are not using the correct format: \"hh:mm\". '

    # return [alarm_confirmation, verified, time]
    return [alarm_confirmation, verified, time]
