import discord
from discord.ext import commands

class CheckType(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='check_type', aliases=['ct', 'checktype'])
    async def _check_type(self, ctx, id):
        if user := self.bot.get_user(id):
            await ctx.reply(embed=discord.Embed(title='Type: User', description=user.mention, color=0x00ffff))
            return
        elif guild := self.bot.get_guild(id):
            await ctx.reply(embed=discord.Embed(title='Type: Guild', description=guild.name, color=0x00ffff))
            return
        elif role := ctx.guild.get_role(id):
            await ctx.reply(embed=discord.Embed(title='Type: Role', description=role.mention, color=0x00ffff))
            return
        elif channel := self.bot.get_channel(id):
            await ctx.reply(embed=discord.Embed(title='Type: Channel', description=channel.mention, color=0x00ffff))
            return
        else:
            await ctx.reply(embed=discord.Embed(title='Coundn\'t find', color=0xff0000))
            return

def setup(bot):
    bot.add_cog(CheckType(bot))
    