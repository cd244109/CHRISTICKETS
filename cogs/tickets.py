import discord
from discord.ext import commands
import chat_exporter
import io
import asyncio
import datetime
from discord_components import *

class tickets(commands.Cog): #replace "example" with cog name

  global guildID
  guildID = 104163051707572224
  global createTicketChan
  createTicketChan = 669902655807815690
  global ticketCategory
  ticketCategory = 877272533416697876
  global transChannel #transcript channel
  transChannel = 669902656227115039
  global AdminRoleName
  AdminRoleName = "MGT Admin"
  global OrgURL
  OrgURL = "http://mgtrolls.eu/"
  global OrgLogo
  OrgLogo = "https://i.imgur.com/3Ymaqpt.png"
  global AdminRole
  AdminRole = "104165720035708928"
  global TicketMessage
  TicketMessage = "Thank you for creating a ticket with MGT. One of our staff members will review your ticket and assist you as soon as possible. In the meantime please provide any additional details or description of your issue."

  def __init__(self, client):
    self.client = client
    self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

  def get_ratelimit(self, message: discord.Message):
    """Returns the ratelimit left"""
    bucket = self._cd.get_bucket(message)
    return bucket.update_rate_limit()
  
  intents = discord.Intents.default()
  intents.members = True

  #events
  @commands.Cog.listener()
  async def on_ready(self):
    print('tickets.py cog loaded')
    guild = self.client.get_guild(guildID)
    msg = guild.get_channel(createTicketChan)
    await msg.purge(limit=2)
    #CUSTOMIZE THIS EMBED:
    embed = discord.Embed(title="MGT Bot", color=0xff0000)
    embed.set_thumbnail(url="https://i.imgur.com/3Ymaqpt.png")
    embed.add_field(name="Thanks for playing on MGT", value="Click the buttown below to create a ticket. **Don't click it more than once!**", inline=True)
    chan = guild.get_channel(createTicketChan)
    global createTicketMsg
    createTicketMsg = await chan.send(embed=embed)
    await chan.send(content="‎", components=[Button(style=ButtonStyle.green, label="Create a ticket", custom_id="ticketButton")])
    
  @commands.Cog.listener()
  async def on_button_click(self, interaction):
    global guildID
    global createTicketMsg
    global ticketCategory
    global AdminRoleName
    global OrgURL
    global OrgLogo
    global TicketMessage
    if interaction.component.label == "Create a ticket":
      guild = self.client.get_guild(guildID)
      chans = str(guild.text_channels)
      tickname = str(interaction.author).lower()
      tickname = tickname.replace("#", "")
      print(interaction.author.id)
      print(interaction.author)

      ratelimit = self.get_ratelimit(interaction)
      if ratelimit is None:
        if tickname not in chans:
          category = self.client.get_channel(ticketCategory)
          ticket_channel = await category.create_text_channel(f"{interaction.author}",
                                        topic=f"A ticket for {interaction.author}.",
                                        permission_synced=True)
          guild = self.client.get_guild(guildID)
            
          overwrite = discord.PermissionOverwrite()
          overwrite.send_messages = False
          overwrite.read_messages = False
          overwrite.view_channel = False
            
          await ticket_channel.set_permissions(guild.default_role, overwrite=overwrite)
              
          role = discord.utils.get(guild.roles, name=AdminRoleName)
          await ticket_channel.set_permissions(role, view_channel=True, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
          await ticket_channel.set_permissions(interaction.author, view_channel=True, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

          await ticket_channel.send(f"UserID: {interaction.author.id}")

          embed = discord.Embed(title="Thank you for opening a ticket", url=OrgURL,
                            color=0x00ff33)
          embed.set_thumbnail(url=OrgLogo)
          embed.add_field(name="Confidentiality Notice", value="The contents of this ticket and any attachments "
                            "are intended solely for the ticket creator and "
                            "may contain confidential and/or privileged "
                            "information. If you are not the intended user "
                            "of this ticket or speaking on their behalf, "
                            "or if you have been added to this ticket in "
                            "error, please immediately alert the admins by "
                            "tagging them and not sharing any information or "
                            "attachments from within. Thank you for your "
                            "cooperation.", inline=False)
          await ticket_channel.send(embed=embed)
          await ticket_channel.send(f"{interaction.author.mention} {TicketMessage}")
          await interaction.respond(content='Ticket Created!')
        else:
          await interaction.respond(content='Failed. You already have an open ticket.')
      else:
        await interaction.respond(content='STOP SPAMMING THE BUTTON!')
      
      
      
  @commands.Cog.listener()
  async def on_message(self, message):
    global ticketCategory
    if message.channel.category.id == ticketCategory:
      try:
        name = str(message.channel.id)
        task, = [task for task in asyncio.all_tasks() if task.get_name() == name]
        task.cancel()
      except ValueError or AttributeError:
        return

  @commands.command()
  async def close(self, ctx, *message):
    global transChannel
    global ticketCategory
    global AdminRoleName

    role = discord.utils.get(ctx.guild.roles, name=AdminRoleName)
    transchannel = self.client.get_channel(transChannel)
    reason = message[0:]
    tidyreason = (','.join(reason).replace(",", " "))

    if role in ctx.author.roles:
        if ctx.channel.category.id == ticketCategory:
            transcript = await chat_exporter.export(ctx.channel)
            if transcript is None:
                return
            transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                           filename=f"transcript-{ctx.channel.name}.html")

            await transchannel.send(f"Ticket closed. Reason: {tidyreason}" + " | " + str(ctx.channel.name) + " | Closed at " + str(datetime.datetime.utcnow()) + "z" , file=transcript_file)

            word = "UserID:"
            messages = await ctx.channel.history(limit=2000).flatten()

            for msg in messages:
                if word in msg.content:
                    if "UserID" in msg.content:
                        UserID = int(msg.content[8:])                    
                        guild = self.client.guilds[0]
                        try:
                          member = await guild.fetch_member(UserID)
                          user = await member.create_dm()
                        except:
                          print("member not found. user likely left discord")

                        transcript = await chat_exporter.export(ctx.channel)
                        if transcript is None:
                            return
                        transcript_file = discord.File(io.BytesIO(transcript.encode()),
                                                       filename=f"transcript-{ctx.channel.name}.html")

                        try:
                          await user.send(f"Here is your ticket transcript. Closure Reason: {tidyreason}\nPress the download button to view it.", file=transcript_file)
                          print(f"Transcript has also been sent to {member}")
                        except:
                          print("User has DMs blocked or left discord")
                        
            await ctx.channel.delete()
        else:
            await ctx.send("You can only use this command within a ticket")
    else:
        if ctx.channel.category.id == ticketCategory:
            await ctx.send(f'<@&{AdminRole}> have been notified you wish to close your ticket.')
        else:
            return

  @commands.command()
  async def autoclose(self, ctx):
    global transChannel
    global ticketCategory
    global AdminRoleName
    
    role = discord.utils.get(ctx.guild.roles, name=AdminRoleName)

    if ctx.channel.category.id != ticketCategory:
      await ctx.send("This command can only be used in a ticket channel")
    else:
      role = discord.utils.get(ctx.guild.roles, name=AdminRoleName)
      if role not in ctx.author.roles:
        await ctx.send("You do not have permission to use this command")
      else:
        await ctx.send("Autoclose enabled. Ticket will close in 12 hours unless another message is sent.")

        async def autocloseTask():
          
          try:
            await asyncio.sleep(43200)
            transcript = await chat_exporter.export(ctx.channel)
            if transcript is None:
              return
            transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"transcript-{ctx.channel.name}.html")
            
            channel1 = self.client.get_channel(transChannel)
                
            await channel1.send(f"Ticket closed. Reason: Autoclosed" + " | " + str(ctx.channel.name) + " | Closed at " + str(datetime.datetime.utcnow()) + "z", file=transcript_file)

            word = "UserID:"
            messages = await ctx.channel.history(limit=2000).flatten()

            for msg in messages:
              if word in msg.content:
                if "UserID" in msg.content:
                  UserID = int(msg.content[8:])                    
                  guild = self.client.guilds[0]
                  try:
                    member = await guild.fetch_member(UserID)
                    user = await member.create_dm()
                  except:
                    print("member not found. user likely left discord")
                  transcript = await chat_exporter.export(ctx.channel)
                  if transcript is None:
                    return
                  transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{ctx.channel.name}.html")

                  try:
                    await user.send(f"Here is your ticket transcript. Closure Reason: Autoclosed\nPress the download button to view it.", file=transcript_file)
                    print(f"Transcript has also been sent to {member}")
                  except:
                    print("User has DMs blocked or left discord")
                                
                  await ctx.channel.delete()
          except asyncio.CancelledError:
            await ctx.send("Autoclose Cancelled!")
      await asyncio.create_task(autocloseTask(), name=str(ctx.channel.id))
    
  @commands.command()
  async def adduser(self, ctx, member: discord.Member):
    global ticketCategory
    global AdminRole
    role = discord.utils.get(ctx.guild.roles, name="MGT Admin")

    if role in ctx.author.roles:
        if ctx.channel.category.id == ticketCategory:
            try:
              await ctx.message.channel.set_permissions(member, read_messages=True, read_message_history=True, send_messages=True)
              await ctx.send(f"{member} added to the ticket")
            except:
              await ctx.send("Error!")
        else:
            await ctx.send("You can only use this command within a ticket")
    else:
        if ctx.channel.category.id == ticketCategory:
            await ctx.send(f'Only <@&{AdminRole}> can add users to a ticket.')
        else:
            return

def setup(client):
  client.add_cog(tickets(client))
