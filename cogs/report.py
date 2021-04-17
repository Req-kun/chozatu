import discord
from discord.ext import commands
import traceback
siteihouhou = '''コマンド構文: ```
report [<ChannelID>-<MessageID> / <MessageURL>]

alias: repo
```'''

def create_embed(rep_msg, msg):
    embed_f = discord.Embed(
        title='メッセージが通報されました',
        description=f'通報者: {rep_msg.author.mention}\n通報時間: {rep_msg.created_at}\nメッセージ作成時間: {msg.created_at}\n\n[メッセージへジャンプ]({msg.jump_url})'
    )
    
    embed_s = discord.Embed(
        description=f'{msg.content}',
    ).set_author(
        name=f'{msg.author.display_name}({msg.author.id})',
        icon_url=msg.author.avatar_url,
    )
    return [embed_f, embed_s]
    
class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['repo'])
    async def report(self, ctx, msg):
        try:
            msg = await self.bot.fetch_message(msg)
        except:
            print(traceback.format_exc())
            await ctx.send(embed=discord.Embed(title='メッセージが見つかりませんでした', color=0xff0000,
            description=siteihouhou))
            return
        
        await self.bot.report_wh.send(embeds=create_embed(ctx.message, msg))
        await ctx.message.add_reaction('👍')
        return
        
def setup(bot):
    bot.add_cog(Report(bot))
