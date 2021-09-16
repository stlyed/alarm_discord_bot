# welcome to my discord bot
from discord.ext import commands, tasks
import os

import variables
import help

import alarm.main as main_alarm
import alarm.in_alarm as in_alarm


def main():
    # initialize discord bot
    bot = commands.Bot(command_prefix='!')

    # check when bot is ready
    @bot.event
    async def on_ready():
        # start checking if there is an alarm ringing as soon as bot is ready
        check_alarm.start()

    # background task to check if an alarm is ringing
    @tasks.loop(seconds=1, count=None)
    async def check_alarm():
        channel = bot.get_channel(int(variables.get_secret('DISCORD_CHANNEL_ID')))
        is_in_alarm = in_alarm.in_alarm()
        if is_in_alarm != 'None':
            await channel.send(is_in_alarm)

    # responding to messages
    @bot.event
    async def on_message(message):

        # ignore the message that is being sent by the bot
        if message.author != bot.user:
            # give the user all the commands
            if message.content.startswith('!help'):
                await message.channel.send(help.help)

            # everything that has to do with alarm
            if message.content.startswith('!alarm'):
                await message.channel.send(main_alarm.alarm(message.author.mention, message.content))

    # send discord bot live
    bot.run(variables.get_secret('DISCORD_TOKEN_ID'))


if __name__ == '__main__':
    main()

# await bot.fetch_user(258694976999784450)  # get username based on user id
