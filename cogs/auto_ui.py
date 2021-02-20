import discord
from discord.ext import commands
from discord_embed_extensions import make
import asyncio
import re


class Autoui(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.channel.id == 739056631647830076:
            return

        async for msg in self.bot.unei_ch.history(limit=100):
            if not msg.author.id == 804649928638595093:
                continue
            if len(msg.embeds) > 0:
                embed = msg.embeds[0]
                if not embed.title == 'ユーザ情報':
                    continue
                if embed.author.name.endswith(f'{str(message.author.id)})'):
                    await msg.edit(embed=make(
                        title='ユーザ情報',
                        description='この情報で表示されている時間情報はUTCを用いられています。\n日本(東京)時間への変換は `+9時間` してください。',
                        author={"name": f'{message.author.name}(ID:{message.author.id})', "icon_url": message.author.avatar_url},
                        fields=[
                            {"name": "アカウント作成日時", "value": message.author.created_at},
                            {"name": "サーバー参加日時", "value": message.author.joined_at},
                            {"name": "認証情報", "value": message.content, "inline": False}
                        ],
                        footer={"text": f"-approve {message.author.id}"}
                    ))
                    return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        await self.bot.unei_ch.send(
            embed=make(
                title='ユーザ情報',
                author={"name": f"{member.name}(ID: {member.id})", "icon_url": member.avatar_url},
                description='認証情報送信待機中…'
            )
        )
        """
        await self.bot.unei_ch.send(
            embed=make(
                title='ユーザ情報',
                description='この情報で表示されている時間情報はUTCを用いられています。\n日本(東京)時間への変換は `+9時間` してください。',
                author={"name": f'{member.name}(ID:{member.id})', "icon_url": member.avatar_url},
                fields=[
                    {"name": "アカウント作成日時", "value": member.created_at},
                    {"name": "サーバー参加日時", "value": member.joined_at},
                    {"name": "ステータス", "value": status_dict[str(member.status)]},
                    {"name": "ロール", "value": ', '.join([r.mention for r in member.roles])}
                ]
            ))
        """

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return
        async for msg in self.bot.unei_ch.history(limit=100):
            if not msg.author.id == 804649928638595093:
                continue
            if len(msg.embeds) > 0:
                embed = msg.embeds[0]
                if not embed.title == 'ユーザ情報':
                    continue
                if embed.author.name.endswith(f'{str(member.id)})'):
                    await msg.edit(embed=make(
                        title='サーバー脱退済み',
                        author={"name": embed.author.name, "icon_url": embed.author.icon_url}
                    ))
                    return

def setup(bot):
    return bot.add_cog(Autoui(bot))
