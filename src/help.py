from discord import Embed, Color


def embed():
    embed = Embed(
        title='Alarm Discord Bot',
        description='This bot allows you to set an alarm.',
        color=Color.random()
    )
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/883036208836538479/7b963c04c99f50fea9369378320febe0.png?size=128'
    )
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

    return embed
