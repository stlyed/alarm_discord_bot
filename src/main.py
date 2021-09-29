#!/usr/bin/env python3
import discord
from discord.ext import commands, tasks

import secrets

import main_routes as main_alarm
import alarm_ringing as alarm_ringing
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
                embed = discord.Embed(
                    title='Alarm Discord Bot',
                    description='This bot allows you to set an alarm.',
                    color=discord.Color.random()
                )
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/avatars/883036208836538479/7b963c04c99f50fea9369378320febe0.png?size=128')
                embed.add_field(
                    name='!alarm -set',
                    value='create a new alarm.\n'
                          '!alarm -set [hh:mm] [mm-dd-yyyy] ["Alarm Name"] [Mention] \n'
                          'only [hh:mm] is mandatory; "Alarm Name" must be in double quotes.',
                    inline=False
                )
                embed.add_field(
                    name='!alarm -view',
                    value='See all currently active alarms that you have set.',
                    inline=True
                )
                embed.add_field(
                    name='!alarm -view all',
                    value='See all currently active alarms that is in the database.\n',
                    inline=True
                )
                embed.add_field(
                    name='!alarm -edit ',
                    value='Edit an alarm in the database {currently does\'nt work}.\n',
                    inline=False
                )
                embed.add_field(
                    name='!alarm -delete',
                    value='Delete an alarm from the database, {currently does\'nt work}.\n'
                          '!alarm -delete [Alarm Id] \n'
                          'the ID can be found from !alarm -view ',
                    inline=True
                )
                embed.add_field(
                    name='!alarm -delete all',
                    value='Delete all alarm for a user from the database, {currently does\'nt work}.\n'
                          '!alarm -delete [@author]',
                    inline=True
                )
                await message.channel.send(embed=embed)

            # everything that has to do with alarm
            if message.content.startswith('!alarm'):
                await message.channel.send(main_alarm.alarm(message.author.mention, message.content))

    # send discord bot live
    bot.run(discord_token_id)


if __name__ == '__main__':
    main()
