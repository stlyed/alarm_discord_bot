'''
This is the main file for all user request/commands relating alarms
it gets the alarm command and sends to the proper file to get process
Get the processed result and send back to user
'''

from alarm.alarm_set import alarm_set  # my files


def alarm(author, message):
    alarm_confirmation = None

    # give help if the command is the only thing typed
    if message == '!alarm':
        alarm_confirmation = 'Here are all the commands included into \"!alarm\":\n' \
                             '     !alarm -set\n' \
                             '     !alarm -view\n' \
                             '     !alarm -view all\n' \
                             '     !alarm -edit\n' \
                             '     !alarm -delete\n' \
                             '     !alarm -delete all\n' \

    # create new alarm
    elif '!alarm -set' in message:
        # !alarm -set will show help page if typed alone
        if message == '!alarm -set':
            alarm_confirmation = 'hh:mm {mm-dd-yyyy} "alarm name" mention \n' \
                                 'only hh:mm is mandatory'
        # create a new alarm if there are parameters after !alarm -set
        else:
            alarm_confirmation = alarm_set.alarm_set(message, author)

    return alarm_confirmation
