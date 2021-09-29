#!/usr/bin/env python3
import discord
from discord.ext import commands, tasks

import secrets

import main_routes as main_alarm
import alarm_ringing as alarm_ringing
import help as alarm_help
import alarm_class


def main():
    # initialize discord bot
    bot = commands.Bot(command_prefix='!')
    discord_channel_id = int(secrets.get_secret('DISCORD_CHANNEL_ID'))
    discord_token_id = secrets.get_secret('DISCORD_TOKEN_ID')

    # check when bot is ready
    @bot.event
    async def on_ready():
        # start checking if there is an alarm ringing as soon as bot is ready
        check_alarm.start()

    # background task to check if an alarm is ringing
    @tasks.loop(seconds=20, count=None)
    async def check_alarm():
        channel = bot.get_channel(discord_channel_id)
        if alarm_ringing.alarm_ringing()[0] != 'None':
            await channel.send(str(alarm_ringing.alarm_ringing()[0]))
            alarm_class.Alarm().delete_from_db(alarm_ringing.alarm_ringing()[1])

    # responding to messages
    @bot.event
    async def on_message(message):

        # ignore the message that is being sent by the bot
        if message.author != bot.user:
            # give the user all the commands
            if message.content.startswith('!help'):
                await message.channel.send(embed=alarm_help.embed())

            # everything that has to do with alarm
            if message.content.startswith('!alarm'):
                await message.channel.send(main_alarm.alarm(message.author.mention, message.content))

    # send discord bot live
    bot.run(discord_token_id)


if __name__ == '__main__':
    main()
