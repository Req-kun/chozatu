from discord.ext import commands
import discord


class Ng_word(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ngw')
    @commands.has_permissions(administrator=True)
    async def _ngw(self, ctx, mode):
        await ctx.message.delete()
        if not mode in ['add', 'remove']:
            await ctx.send('無効なモードです\n使用可能なモード: `add`, `remove`', delete_after=10.0)
        sentence = ctx.message.content[len(f'{ctx.prefix}ngw {mode} '):]
        if mode == 'add':
            if sentence in self.bot.ng_words:
                await ctx.send('すでに追加されています', delete_after=10.0)
                return
            else:
                await self.bot.ng_word_ch.send(sentence)
                self.bot.ng_words.append(sentence)
                return
        if mode == 'remove':
            if not sentence in self.bot.ng_words:
                await ctx.send('存在しないNGワードです', delete_after=10.0)
                return
            else:
                async for msg in  self.bot.ng_word_ch.history(limit=None):
                    if msg.content == sentence:
                        await msg.delete()
                        self.bot.ng_words.remove(sentence)
                        return


    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.bot.ready:
            return
        if message.author.bot:
            return
        if message.content.startswith(f'{self.bot.command_prefix}ngw'):
            return
        for ng_word in self.bot.ng_words:
            if ng_word in message.content:
                await message.delete()
                return


def setup(bot):
    bot.add_cog(Ng_word(bot))
