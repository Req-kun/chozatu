import discord
from discord.ext import commands
from discord_embed_extensions import make
import asyncio
import re

status_dict = {
    "offline": "オフライン",
    "online": "オンライン",
    "idle": "退席中",
    "dnd": "取り込み中",
    "do_not_disturb": "取り込み中"
}
class Autoui(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id == 738397603439444028:
            return
        if message.content.endswith('が鯖に来ました'):
            member_ob = message.guild.get_member(int(str(re.sub("\\D", "", message.content))))
            await message.channel.send(
            embed=make(
                title='ユーザ情報',
                description='この情報で表示されている時間情報はUTCを用いられています。\n日本(東京)時間への変換は `+9時間` してください。',
                author={"name": f'{member_ob.name}(ID:{member_ob.id})', "icon_url": member_ob.avatar_url},
                fields=[
                    {"name": "アカウント作成日時", "value": member_ob.created_at},
                    {"name": "サーバー参加日時", "value": member_ob.joined_at},
                    {"name": "ステータス", "value": status_dict[str(member_ob.status)]},
                    {"name": "ロール", "value": ', '.join([r.mention for r in member_ob.roles])}
                ]
            ))

def setup(bot):
    return bot.add_cog(Autoui(bot))
