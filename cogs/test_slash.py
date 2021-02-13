import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext


class Slash(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="operate", guild_ids=[733707710784340100], description='このコマンドは運営専用のコマンドです。',
    options=[
    {
    "name": "command",
    "description": "[normal / n, hidden / h, complete_hidden / ch]",
    "type": 3,
    "required": True
    },
    {
    "name": "content",
    "description": "返す内容",
    "type": 3,
    "required": False
    }
    ])
    async def _test(self, ctx, command, content=''):
        print('aaaaa')
        role = ctx.guild.get_role(738956776258535575)
        if not role in ctx.author.roles:
            await ctx.send(content='このコマンドを使用するには <@&738956776258535575> のロールを所持している必要があります', complete_hidden=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
            return
        content = f'\'{content}\''
        if command in ['normal', 'n']:
            await ctx.send(content=content, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
        elif command in ['hidden', 'h']:
            await ctx.send(content=content, hidden=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
            return
        elif command in ['complete_hidden', 'ch']:
            await ctx.send(content=content, complete_hidden=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
            return
        else:
            await ctx.send(content='不明なコマンドです', complete_hidden=True)
            return



def setup(bot):
    bot.add_cog(Slash(bot))
