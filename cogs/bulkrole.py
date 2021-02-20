import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext

def kekka(option:str, success, already, bot, error, error_reasons):
    if option == 'add':
        if error > 0:
            return f'''
付与成功:
```
{success}
```
既に所持:
```
{already}
```
Bot(非付与):
```
{bot}
```
エラー(付与失敗):
```
{error}
```
エラー理由:
```
{', '.join(error_reasons)}
```
'''

        elif error == 0:
            return f'''
付与成功:
```
{success}
```
既に所持:
```
{already}
```
Bot(非付与):
```
{bot}
```
エラー(付与失敗):
```
{error}
```
'''

    elif option == 'rem':
        if error > 0:
            return f'''
はく奪成功:
```
{success}
```
既に非所持:
```
{already}
```
Bot(非はく奪):
```
{bot}
```
エラー(はく奪失敗):
```
{error}
```
エラー理由:
```
{', '.join(error_reasons)}
```
'''

        elif error == 0:
            return f'''
はく奪成功:
```
{success}
```
既に非所持:
```
{already}
```
Bot(非はく奪):
```
{bot}
```
エラー(はく奪失敗):
```
{error}
```
'''


class Slash_bulk(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_subcommand(base="op", name="bulkrole",
    base_description='運営専用コマンド', description='超雑談鯖オーナー専用コマンド',
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "option",
            "description": "付与/はく奪の選択",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "add",
                    "value": "add"
                },
                {
                    "name": "remove",
                    "value": "remove"
                }
            ]
        },
        {
            "name": "role",
            "description": "付与/はく奪するロール",
            "type": 8,
            "required": True
        }
    ])
    async def _chouzatudan_bulkrole(self, ctx, option, role):
        if ctx.author.id != ctx.guild.owner_id:
            await ctx.send(content=f'このコマンドはサーバーオーナーである {ctx.guild.owner.mention} 専用のコマンドです。', complete_hidden=True, allowed_mentions=discord.AllowedMentions.none())
            return
        channel = ctx.channel
        success = 0
        already = 0
        bot_mem = 0
        error = 0
        error_reasons = []
        if option == 'add':
            for member in ctx.guild.members:
                if member.bot:
                    bot_mem += 1
                    continue
                elif role in member.roles:
                    already += 1
                    continue
                try:
                    await member.add_roles(role)
                    success += 1
                    continue
                except Exception as e:
                    error += 1
                    if not str(e) in error_reasons:
                        error_reasons.append(str(e))
                    continue
            kekka_embed = discord.Embed(title='付与結果',
            description=kekka('add', success, already, bot_mem, error, error_reasons), color=ctx.guild.me.color)
            await ctx.send(embeds=[kekka_embed])
            return

        elif option == 'remove':
            for member in ctx.guild.members:
                if member.bot:
                    bot_mem += 1
                    continue
                elif not role in member.roles:
                    already += 1
                    continue
                try:
                    await member.remove_roles(role)
                    success += 1
                    continue
                except Exception as e:
                    error += 1
                    if not str(e) in error_reasons:
                        error_reasons.append(str(e))
                    continue
            kekka_embed = discord.Embed(title='付与結果',
            description=kekka('rem', success, already, bot_mem, error, error_reasons), color=ctx.guild.me.color)
            await channel.send(embed=kekka_embed)
            return



def setup(bot):
    bot.add_cog(Slash_bulk(bot))
