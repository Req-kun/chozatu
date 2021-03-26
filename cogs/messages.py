import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="fun", name="messges",
    base_description='楽しもう！', description='指定のユーザー/ロールの出現率 (userもしくはroleを指定。(userを指定している場合はroleは無視されます))',
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "limit",
            "description": "計測するメッセージ数(MAX 1000)",
            "type": 4,
            "required": True
        },
        {
            "name": "bot",
            "description": "Botのメッセージもカウントするか",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "yes",
                    "value": "yes"
                },
                {
                    "name": "no",
                    "value": "no"
                }
            ]
        },
        {
            "name": "user",
            "description": "ユーザー",
            "type": 6,
            "required": False
        },
        {
            "name": "role",
            "description": "ロール",
            "type": 8,
            "required": False
        }
    ])
    async def _messages(self, ctx, limit, bot, user = None, role = None):
        await ctx.respond(eat=True)
        if limit > 1000:
            await ctx.send('指定可能な最大メッセージ数は 1000 です', hidden=True)
        if user == None and role == None:
            await ctx.send('userもしくはroleを必ず指定してください', hidden=True)
            return

        elif not user == None:
            keisokunow = await ctx.send(embed=discord.Embed(title='計測中…', color=discord.Colour.dark_theme()))
            try:
                if bot == 'yes':
                    count = 0
                    async for msg in ctx.channel.history(limit=limit):
                        if msg.author.id == user.id:
                            count += 1
                    embed = discord.Embed(
                                title='結果',
                                description=f'{limit} メッセージ中 {count} メッセージ({round(count / limit *100, 1)} %)が指定ユーザーのメッセージです。\nfrom: {ctx.author.mention}\nto: {user.mention}\nbot: {bot}',
                                color=0x00ffff
                            )
                    embed.set_footer(text='チャンネルの総メッセージ数がlimitで指定された値に満たない場合、適切でない値が返される場合があります。')
                    await keisokunow.edit(embed=embed)
                    return

                else:
                    count = 0
                    msg_count = 0
                    async for msg in ctx.channel.history(limit=None):
                        if msg_count > limit:
                            break
                        if msg.author.bot:
                            continue

                        if msg.author.id == user.id:
                            count += 1
                        msg_count += 1

                    embed = discord.Embed(
                                title='結果',
                                description=f'{limit} メッセージ中 {count} メッセージ({round(count / limit *100, 1)} %)が指定ユーザーのメッセージです。\nfrom: {ctx.author.mention}\nto: {user.mention}\nbot: {bot}',
                                color=0x00ffff
                            )
                    embed.set_footer(text='チャンネルの総メッセージ数がlimitで指定された値に満たない場合、適切でない値が返される場合があります。')
                    await keisokunow.edit(embed=embed)
                    return
            except Exception as e:
                await keisokunow.edit(embed=discord.Embed(title='エラー', description=f'```{e}```', color=0xff0000))

        elif user == None and not role == None:
            keisokunow = await ctx.send(embed=discord.Embed(title='計測中…', color=discord.Colour.dark_theme()))
            try:
                if bot == 'yes':
                    count = 0
                    async for msg in ctx.channel.history(limit=limit):
                        if role in msg.author.roles:
                            count += 1
                    embed = discord.Embed(
                                title='結果',
                                description=f'{limit} メッセージ中 {count} メッセージ({round(count / limit *100, 1)} %)が指定ロールのメッセージです。\nfrom: {ctx.author.mention}\nto: {role.mention}\nbot: {bot}',
                                color=0x00ffff
                            )
                    embed.set_footer(text='チャンネルの総メッセージ数がlimitで指定された値に満たない場合、適切でない値が返される場合があります。')
                    await keisokunow.edit(embed=embed)
                    return

                else:
                    count = 0
                    msg_count = 0
                    async for msg in ctx.channel.history(limit=None):
                        if msg_count > limit:
                            break
                        if msg.author.bot:
                            continue

                        if role in msg.author.roles:
                            count += 1
                        msg_count += 1

                    embed = discord.Embed(
                                title='結果',
                                description=f'{limit} メッセージ中 {count} メッセージ({round(count / limit *100, 1)} %)が指定ロールのメッセージです。\nfrom: {ctx.author.mention}\nto: {role.mention}\nbot: {bot}',
                                color=0x00ffff
                            )
                    embed.set_footer(text='チャンネルの総メッセージ数がlimitで指定された値に満たない場合、適切でない値が返される場合があります。')
                    await keisokunow.edit(embed=embed)
                    return
            except Exception as e:
                await keisokunow.edit(embed=discord.Embed(title='エラー', description=f'```{e}```', color=0xff0000))


def setup(bot):
    bot.add_cog(Messages(bot))
