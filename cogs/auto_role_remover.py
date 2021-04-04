import discord
from discord.ext import commands
import datetime

class AutoRoleRemover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # {prefix}{command_name} {user_id 123} {role_id 456} {timeoptions 59m(inutes) 23h(ours) 364d(ays)}
    @commands.command(aliases=['autorroleremover', 'auto_role_remove', 'arr'])
    @commands.has_permissions(manage_roles=True)
    async def auto_role_remover(self, ctx, user: discord.Member, role: discord.Role, *timeoptions):
        for timeoption in timeoptions:
            if len([t for t in timeoptions if t[-1] == timeoption[-1]]) > 1:
                await ctx.send(embed=discord.Embed(title='同じ時間単位が複数与えられています', color=0xff0000))
                return
        minutes = '0m'
        hours = '0h'
        days = '0d'
        weeks = '0w'
        for timeoption in timeoptions:
            if timeoption.endswith('m'):
                minutes = timeoption
            elif timeoption.endswith('h'):
                hours = timeoption
            elif timeoption.endswith('d'):
                days = timeoption
            elif timeoption.endswith('w'):
                weeks = timeoption
        delta = datetime.timedelta(minutes=int(minutes[:-1]), hours=int(hours[:-1]), days=int(days[:-1]), weeks=weeks[:-1])
        now = datetime.datetime.utcnow()
        tyming = now + delta
        msg = await self.bot.time_remove_role_ch.send(f'{user.id}/{role.id}/{tyming}')
        self.bot.time_remove_role[tyming] = dict(user_id=user.id, role_id=role.id, message=msg)
        await ctx.send(embed=discord.Embed(title=f'ロール自動削除を追加しました', description=f'時間: {tyming}(UTC)\nロール: {role.mention}\n対象: {user.mention}', color=0x00ffff))
        
        
def setup(bot):
    bot.add_cog(AutoRoleRemover(bot))
