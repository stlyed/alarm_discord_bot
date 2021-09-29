#!/usr/bin/env python3
import datetime
import hashlib
import boto3
from boto3.dynamodb.conditions import Attr

import verify_user_input


class Alarm:
    def __init__(self, **kwargs):
        # the body of the message
        self.message = kwargs.get('message')

        # if there was a message, then retrieve data from it
        if self.message is not None:
            # get the author of the message
            self.author = kwargs.get('author')
            # create confirmation message
            self.confirmation = ['', True]

            # check if user specified an alarm name
            alarm_name = [i for i in range(len(self.message)) if self.message.startswith('"', i)]
            # alarm name is everything from the first quote to the last if user specified an alarm name
            alarm_name = self.message[alarm_name[0] + 1:alarm_name[-1]] if len(alarm_name) > 1 else self.author
            self.alarm_name = alarm_name

            # get the time for alarm
            time = self.message[self.message.find(':', 10, 19) - 2:self.message.find(':', 10, 19) + 3]
            # convert time to 24 hour and if not successful, add to confirmation message
            if not verify_user_input.convert_time_24h(time, self.message):
                self.confirmation = ['There is a problem with the specified time.\n'
                                     'Check that you are using a supported format.', False]
            self.user_time = verify_user_input.convert_time_24h(time, self.message)

            # have today as default date
            self.alarm_date = str(datetime.date.today().strftime("%m-%d-%Y"))
            # check if user specified a date
            alarm_name = [i for i in range(len(self.message)) if self.message.startswith('-', i)]
            if len(alarm_name) == 3:
                user_date = self.message[alarm_name[1] - 2: alarm_name[2] + 5]
                self.alarm_date = user_date
            # check if the date and time combination is not in the past
            if not verify_user_input.verify_date(self.alarm_date, self.user_time):
                self.confirmation = ['There is a problem with the date/time combination.\n'
                                     'Check that your using a supported format; '
                                     'Check that the combination is not in the past.', False]

            self.user_mention = ''
            # check if user specified any other people to ping/mention
            mention_list = [i for i in range(len(self.message)) if self.message.startswith('@', i)]
            for i in mention_list:
                user_mention = self.message[i - 1:i + 21]
                self.user_mention += user_mention

    def upload_to_db(self):
        # if there was no error above, upload to database
        if self.confirmation[1]:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Alarms_for_discordBot')

            # generate random alarm id
            m = hashlib.md5()
            m.update(self.message.encode())
            # put data in a dictionary
            data = {
                'Alarm Id': str(int(m.hexdigest(), 16))[0:12],
                'Author': self.author,
                'Alarm Name': self.alarm_name,
                'Date': self.alarm_date,
                'Time': self.user_time,
                'Mention': self.user_mention
            }.copy()

            # make sure that alarm was not already created
            response = table.scan(
                FilterExpression=Attr('Alarm Name').eq(self.alarm_name) &
                                 Attr('Date').eq(self.alarm_date) &
                                 Attr('Time').eq(self.user_time)
            )
            if data not in response['Items']:
                # add the alarm if it was not created already
                table.put_item(Item=data)
                # tell the user that data has been successfully imported
                self.confirmation[0] = f'Alarm for {self.alarm_name} has been created for:' \
                                       f' {verify_user_input.convert_time_12h(self.user_time)} on {self.alarm_date}.\n'
                if data["Mention"] != '':
                    self.confirmation[0] += f'I will also call {data["Mention"]}.'
            else:
                self.confirmation[0] = f'You have previously created and alarm named \"{data["Alarm Name"]}\" for: ' \
                                    f'{data["Time"]} on {data["Date"]}'
                self.confirmation[1] = False

        return self.confirmation

    @staticmethod
    def delete_from_db(alarm_id):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Alarms_for_discordBot')

        # delete syntax
        table.delete_item(
            Key={
                'Alarm Id': alarm_id
            }
        )

        return f'Alarm has been successfully deleted'

    @staticmethod
    def retrieve_from_db():
        # Get the service resource.
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Alarms_for_discordBot')

        # get every item from the table
        response = table.scan()

        return response['Items']
