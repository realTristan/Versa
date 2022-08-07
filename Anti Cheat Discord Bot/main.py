from discord.ext import commands
import discord, os

# // Bot Permissions
client = commands.Bot(
    command_prefix='=', 
    intents=discord.Intents(
        messages=True, 
        guilds=True, 
        members=True, 
        presences=True
    )
)
client.remove_command('help')

# // Command Errors
@client.event
async def on_command_error(_, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        return
    raise error

# // On Bot Ready
@client.event
async def on_ready():
    print(f'Launched: {client.user.name} // {client.user.id}')
    await client.change_presence(activity=discord.Game(name="=key / =key @user"))

# // Load cogs
for filename in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cogs')):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded: cog.{filename[:-3]}')

client.run('YOUR BOT TOKEN')