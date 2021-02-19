import discord
from discord.ext import commands
import aiohttp
import io
class Pin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='pin')
    @commands.has_permissions(administrator=True)
    async def _pin(self, ctx, message_id):
        message = await ctx.channel.fetch_message(int(message_id))
        if len(message.attachments) > 0:
            async with aiohttp.ClientSession() as session:
                for atchmt in message.attachments:
                    async with session.get(atchmt.url) as r:
                        data = io.BytesIO(await r.read())
                        files.append(discord.File(data, atchmt.filename))
        await self.bot.pin_webhook.send(
            embeds=message.embeds,
            content=message.content,
            username=f"{message.author.display_name}(ID:{message.author.id})",
            avatar_url=message.author.avatar_url,
            files=files
        )
        return

def setup(bot):
    return bot.add_cog(Pin(bot))
