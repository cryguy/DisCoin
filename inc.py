import discord

def embednorm(message):
    embed = discord.Embed(description=message, color=0x00a0ea)
    return embed

def embederr(message):
    embed = discord.Embed(description=message, color=0xe62845)
    return embed