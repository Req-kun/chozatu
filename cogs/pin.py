import discord
from discord.ext import commands
import aiohttp
import io
class Pin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            if payload.guild_id != 733707710784340100:
                return
            if payload.member.bot:
                return
            if payload.guild_id != self.bot.guild.id:
                return
            if str(payload.emoji) == "📌":
                payload.guild = self.bot.get_guild(payload.guild_id)
                payload.channel = self.bot.get_channel(payload.channel_id)
                payload.message = await payload.channel.fetch_message(payload.message_id)
                if payload.message.author.id != 804649928638595093:
                    return
                member = payload.member
                files = []
                if not member.guild_permissions.administrator:
                    return
                if len(payload.message.attachments) > 0:
                    async with aiohttp.ClientSession() as session:
                        for atchmt in payload.message.attachments:
                            async with session.get(atchmt.url) as r:
                                data = io.BytesIO(await r.read())
                                files.append(discord.File(data, atchmt.filename))
                await self.bot.pin_webhook.send(
                    embeds=payload.message.embeds,
                    content=payload.message.content,
                    username=f"{payload.message.author.display_name}(ID:{payload.message.author.id})",
                    avatar_url=payload.message.author.avatar_url,
                    files=files
                    )
                return
        except Exception as e:
            await payload.channel.send(embed=discord.Embed(title='Error', description=f'```{e}```', color=0xff0000))


def setup(bot):
    return bot.add_cog(Pin(bot))
