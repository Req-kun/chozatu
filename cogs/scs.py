import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from random import randint

class Scs(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True, sync_commands=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_subcommand(base="fun", name="scs",
    base_description="楽しもう！", description="サーバーのロゴたち",
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "mode",
            "description": "画像を追加/表示 ※追加は運営のみ可能",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "add",
                    "value": "add"
                },
                {
                    "name": "send",
                    "value": "send"
                }
            ]
        },
        {
            "name": "image_url",
            "description": "追加する画像のURL(モードで`send`を選択していた場合は無視されます)",
            "type": 3,
            "required": False
        }
    ])
    async def _scs(self, ctx, mode, image_url = ''):

        if mode == 'add':
            if not self.bot.unei_role in ctx.author.roles:
                await ctx.send(content='画像の追加は運営のみ可能となっています。', complete_hidden=True)
                return
            if image_url in self.bot.scs_images:
                await ctx.send(content='この画像は既に登録されています。', complete_hidden=True)
                return
            if not image_url.startswith('https://'):
                await ctx.send(content='画像はURLで指定してください。', complete_hidden=True)
                return
            await self.bot.scs_backup.send(content=image_url)
            self.bot.scs_images.append(image_url)
            await ctx.send(content='画像の追加が完了しました。', complete_hidden=True)
            return
        if mode == 'send':
            await ctx.send(content=self.bot.scs_images[randint(0, len(self.bot.scs_images)-1)])
            return


def setup(bot):
    bot.add_cog(Scs(bot))
