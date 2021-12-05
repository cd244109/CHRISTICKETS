This repository contains the code for a discord ticket bot coded in python.

Instructions for use:
1. Set your bot token at the bottom of main.py
2. Set Categories and channel permissions appropriately. Tickets should have their own category and hidden from all users aside from admins. The create a ticket channel should be in a different category. 
3. Set all variables in /cogs/tickets.py: (NOTE: All ID variables can be found by right clicking the appropriate object while discord has developer mode enabled)
  1. GuildID
  2. Create a Ticket Channel ID (I suggest the create a ticket channel not be located in the same category as the tickets)
  3. Ticket Category ID (I suggest Tickets have their own dedicated category with appropriate permissions to protect privacy)
  4. Transcript Channel ID (Private channel where all ticket transcripts will be sent when closed)
  5. Admin Role Name
  6. Organization URL (website)
  7. Organization Logo (url)
  8. Admin Role ID
  9. Ticket Message (Message to be sent to users when the ticket it opened.)
4. Install appropriate python libraries and run the bot. 
