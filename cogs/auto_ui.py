import discord
from discord.ext import commands
from discord_embed_extensions import make
import asyncio
import re
import datetime

user_id_pat = re.compile(r'-approve (?P<user_id>[0-9]*)$')

class Delta_to:
    def __init__(self, day, hour, min, sec, milli, micro):
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec
        self.milli = milli
        self.micro = micro
    def __str__(self):
        return f"Delta_to(day={self.day}, hour={self.hour}, min={self.min}, sec={self.sec}, milli={self.milli}, micro={self.micro})"

def trans(delta):
    day = delta.days

    hour = delta.seconds // 3600

    min = (delta.seconds - hour * 3600) // 60

    sec = delta.seconds - (hour * 3600) - (min * 60)

    milli = int(delta.microseconds / 1000)
    micro = int(delta.microseconds - milli * 1000)
    return Delta_to(day, hour, min, sec, milli, micro)


class Autoui(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    """ 認証メッセージ送信 """
    @commands.Cog.listener()
    async def on_message(self, message):
        # 超雑談鯖以外をはじく
        if not message.guild.id == 733707710784340100:
            return

        # Botをはじく
        if message.author.bot:
            return

        # 認証部屋以外をはじく
        if not message.channel.id == 826353003984191538:
            if message.channel.id == 815906779736178728 and message.content.startswith('-approve'):
                id = user_id_pat.match(message.content).group('user_id')
                async for msg in self.bot.approve_ch.history(limit=100):
                    # 専属Bot以外をはじく
                    if not msg.author.id == 804649928638595093:
                        continue
        
                    # 送信待機メッセージ判定１
                    if len(msg.embeds) > 0:
                        embed = msg.embeds[0]
        
                        # 送信待機メッセージ判定２
                        if not embed.title == 'ユーザ情報':
                            continue
        
                        # 送信待機メッセージ判定３
                        if embed.author.name.endswith(f'{id})'):
                            await msg.edit(embed=discord.Embed(title='approved').set_author(name=f'{msg.author.name}(ID:{msg.author.id})', icon_url=msg.author.avatar_url))
                            return
            return
        
        await message.author.add_roles(self.bot.wait_until_approve_role)
        
        # 送信待機メッセージをさがす
        async for msg in self.bot.approve_ch.history(limit=100):
            # 専属Bot以外をはじく
            if not msg.author.id == 804649928638595093:
                continue

            # 送信待機メッセージ判定１
            if len(msg.embeds) > 0:
                embed = msg.embeds[0]

                # 送信待機メッセージ判定２
                if not embed.title == 'ユーザ情報':
                    continue

                # 送信待機メッセージ判定３
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
                        footer={"text": f"-approve {message.author.id}"},
                        color=0x00ffff
                    ))
                    return


    """ サーバー参加 """
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # 超雑談鯖以外をはじく
        if not member.guild.id == 733707710784340100:
            return

        # Botをはじく
        if member.bot:
            return

        # 送信待機メッセージを送信
        await self.bot.approve_ch.send(
            embed=make(
                title='ユーザ情報',
                author={"name": f"{member.name}(ID: {member.id})", "icon_url": member.avatar_url},
                description='認証情報送信待機中…',
                fields=[
                    {"name": "アカウント作成日時", "value": member.created_at},
                    {"name": "サーバー参加日時", "value": member.joined_at}
                ],
                footer={"text": f"-approve {member.id}"}
            )
        )


    """ サーバー離脱 """
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # 超雑談鯖以外をはじく
        if not member.guild.id == 733707710784340100:
            return

        # Botをはじく
        if member.bot:
            return

        # 送信待機メッセージ / ユーザ情報メッセージをさがす
        async for msg in self.bot.approve_ch.history(limit=100):
            # 専属Bot以外のメッセージをはじく
            if not msg.author.id == 804649928638595093:
                continue

            # 判定１
            if len(msg.embeds) > 0:
                embed = msg.embeds[0]

                # 判定２
                if not embed.title == 'ユーザ情報':
                    continue

                # 判定３
                if embed.author.name.endswith(f'{str(member.id)})'):
                    now = datetime.datetime.now()
                    joined = member.joined_at
                    delta = now - joined
                    r = trans(delta)

                    await msg.edit(embed=make(
                        title='サーバー脱退済み',
                        author={"name": embed.author.name, "icon_url": embed.author.icon_url},
                        description=f"{r.day}日{r.hour}時間{r.min}分{r.sec}秒{r.milli}ミリ秒{r.micro}マイクロ秒"
                    ))
                    return

def setup(bot):
    return bot.add_cog(Autoui(bot))
