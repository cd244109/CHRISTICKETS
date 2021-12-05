import discord
from discord.ext import commands, tasks
import datetime
import asyncio

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", case_insensitive=True)
client.remove_command('help')


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
  DiscordComponents(client)
  print("ChrisTickets Started")
  
# always keep this at the bottom of the file for easy access
@client.command()
async def ver(ctx):
    await ctx.send("Bot Version: 1.0 - TicketMaster")


client.run('TOKEN')
