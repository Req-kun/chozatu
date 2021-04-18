"""
text = guild.get_member(699414261075804201).display_name
print(text)
#文字化け
mojibake = text.encode(encoding='utf-8').decode(encoding='shift-jis', errors="ignore")
print(mojibake)
#治す ※完全に修復できない可能性あり
kaijo = mojibake.encode(encoding='shift-jis').decode(encoding='utf-8', errors="ignore")
print(kaijo)
"""

import discord
from discord.ext import commands

class Mojibake(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['文字化け'])
    async def mojibake(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(embed=discord.Embed(title='サブコマンドを指定してください', description='repair: 修復\nbreak: 破壊'))
            return

    # roleコマンドのサブコマンド
    # 指定したユーザーに指定した役職を付与する。
    @mojibake.command(name='repair')
    async def _repair(self, ctx, body):
        await ctx.reply(body.encode(encoding='shift-jis').decode(encoding='utf-8', errors="ignore"))
        return
    
    @mojibake.command(name='break')
    async def _break(self, ctx, body):
        await ctx.reply(body.encode(encoding='utf-8').decode(encoding='shift-jis', errors="ignore"))
        return


def setup(bot):
    bot.add_cog(Mojibake(bot))
