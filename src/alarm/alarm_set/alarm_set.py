'''
this file will create new alarms with the given parameters from the user
it verifies that every input is valid
and inputs it into a file with all the alarms
'''

import datetime

import alarm.alarm_set.verify_time as verify_time
import alarm.alarm_set.verify_date as verify_date
import alarm.alarm_set.new_alarm as new_alarm


# set a new alarm
def alarm_set(message, author):
    today = datetime.date.today().strftime("%m-%d-%Y")  # will have today as default
    data = [author]

    # get the time for alarm
    time = message[message.find(':', 10, 19) - 2:message.find(':', 10, 19) + 3]
    # make sure that time is not greater than 24 hours and other checks
    alarm_confirmation = verify_time.verify_time(time, message)
    # if errors during confirmation stop
    if not alarm_confirmation[1]:
        return alarm_confirmation[0]
    # send time to list for inputting into file
    data.append(alarm_confirmation[2])
    alarm_confirmation = alarm_confirmation[0]

    # check if user specified an alarm name
    alarm_name = [i for i in range(len(message)) if message.startswith('"', i)]
    # if user only put one double quote or they put 2 quotes right next to each other
    if len(alarm_name) == 1 or \
            (len(alarm_name) == 2 and alarm_name[0] + 1 == alarm_name[-1]):
        return f'You must have at least 2 double quotes with a character inside to create a valid alarm name.\n' \
               f'Otherwise, it can left be blank for no alarm'
    # alarm name is everything from the first quote to the last if user specified an alarm name
    alarm_name = message[alarm_name[0] + 1:alarm_name[-1]] if len(alarm_name) > 1 else author
    # add for user confirmation
    alarm_confirmation = f'Alarm for \"{alarm_name}\" has been created for: ' + alarm_confirmation
    # send to list for inputting into file
    data.append(alarm_name)

    # check if user added a date to the alarm
    if message.find('{') > 0 and message.find('}') > 0:
        today = message[message.find('{') + 1:message.find('}')]
        # make sure date is valid
        date_verify = verify_date.verify_date(today)
        # if not verified successfully, stop
        if not date_verify[1]:
            return date_verify[0]
        alarm_confirmation += date_verify[0]
    else: alarm_confirmation += f'on {today}. \n'
    # send to list for inputting into file
    data.append(today)

    # check if user is mentioning anyone else
    mention_list = [i for i in range(len(message)) if message.startswith('@', i)]
    for i in mention_list:
        user_mention = message[i - 1:i + 21]
        if len(data) == 4: data.append(user_mention)
        elif len(data) == 5: data[4] += user_mention
    # tell the user the additional mentions if there are any
    if len(mention_list) >= 1:
        alarm_confirmation += f'This alarm will mention: {data[4]}. '

    # upload alarm to file, check if date and time already past
    # or if they already exist in the file
    alarm_confirmation = new_alarm.upload_to_csv(data, alarm_confirmation)

    return alarm_confirmation
