import discord, base64, string, random, datetime
from discord.ext import commands
from discord.utils import get

class Versa(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    # // Function to send vac embed to channel
    async def send_channel_embed(self, ctx: commands.Context, channel, webhook: discord.Webhook, vac_key: str):
        embed = discord.Embed(title="Versa Anti Cheat", color=16711758, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Webhook Name", value=str(webhook.name))
        embed.add_field(name="Webhook Created", value=str(datetime.datetime.now().strftime('%A %d %B %Y')))
        embed.add_field(name="Webhook Channel", value="#" + str(webhook.channel))
        embed.add_field(name="Webhook URL", value=str(webhook.url))
        embed.add_field(name="VAC Key", value=str(vac_key))
        embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
        await channel.send(embed=embed)
    
    # // Function to send vac embed to user
    async def send_user_embed(self, ctx: commands.Context, user: discord.Member, webhook: discord.Webhook, vac_key: str):
        embed = discord.Embed(title=f"Versa Anti Cheat [{webhook.name}]", url='https://www.mediafire.com/file/75oymy90sydmipy/Versa_Anti_Cheat.zip/file', color=16711758, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="VAC Key", value=str(vac_key))
        embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
        await user.send(embed=embed)
        
    # // Function to get a vac key
    @commands.command()
    async def key(self, ctx: commands.Context, *args):
        user = ctx.author
        if ctx.author.guild_permissions.manage_webhooks:
            if len(list(args)) > 0:
                user = ctx.guild.get_member(int(str(list(args)[0]).strip('>').strip('<').strip('@').replace('!','')))

        # // Get Versa Role / Create new
        role = get(ctx.guild.roles, name="Versa")
        if not role:
            role = await ctx.guild.create_role(name='Versa')

        # // Get Category / Create new and set permissions
        category = get(ctx.guild.categories, name='versa anti cheat')
        if not category:
            category = await ctx.guild.create_category('versa anti cheat')
            await category.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
            await category.set_permissions(role, send_messages=True, read_messages=True)

        # // Get Channel / Create new and create a new webhook
        channel = get(ctx.guild.channels, name=f'{user}')
        if not channel:
            channel = await ctx.guild.create_text_channel(f'{user}', category=category)
        webhook = await channel.create_webhook(name=f"Versa-{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))}")

        # // Create the vac key and send the embed to the channel
        vac_key = base64.b64encode(webhook.url.encode('ascii')).decode('ascii')
        await self.send_channel_embed(ctx, channel, webhook, vac_key)
        await self.send_user_embed(ctx, user, webhook, vac_key)


def setup(client):
    client.add_cog(Versa(client))